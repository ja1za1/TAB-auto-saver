import time

from Command import Command
from ZxLogProcessor import ZxLogProcessor

LOG_FILE_PATH = "PUT THE ZXLOG.txt FILE PATH. USUALLY IN THE SAME FOLDER WHERE SAVES FOLDER IS LOCATED"
SAVES_FOLDER = "PUT THE SAVES FOLDER FILE PATH."
LINES_BETWEEN_SAVE_AND_START_SCREEN = 25  # DON'T CHANGE THIS
MAX_BACKUPS = 5  # MAXIMUM BACKUPS THAT THIS PROGRAM CAN CREATE. WHEN IT REACHES THE MAXIMUM, THE OLDER BACKUP IS ERASED
BACKUP_PREFIX = "Saves_Backup"  # THE PREFIX FOR GENERATED BACKUPS.


def read_tab_log(file_path):
    print(f"Monitoring {file_path}")
    print("Press Ctrl+C to exit...")
    print("-" * 50)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file.seek(0, 2)
            zxLogProcessor = ZxLogProcessor(
                save_folder_path=SAVES_FOLDER, max_backups=MAX_BACKUPS, backup_prefix=BACKUP_PREFIX)
            while True:
                line = file.readline()
                if not line:
                    time.sleep(0.1)
                    continue

                process_line(line, zxLogProcessor)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found!")
    except KeyboardInterrupt:
        print("\n\nClosing program...")


def parse_log_line(line: str):
    """
    Parseia uma linha de log extraindo a mensagem principal.

    Args:
        line (str): Linha completa do log

    Returns:
        str: Mensagem principal limpa
    """
    parts = line.split("-", 2)

    if len(parts) == 2:
        return parts[1].strip()
    elif len(parts) == 3:
        return f"{parts[1].strip()} - {parts[2].strip()}"
    else:
        return line.strip()


def check_command(command_to_check: str):
    # print(f"Command checked - {command_to_check}")
    if command_to_check == Command.SAVING_PROGRESS.value:
        return Command.SAVING_PROGRESS
    elif command_to_check == Command.LOADED_START_SCREEN.value:
        return Command.LOADED_START_SCREEN
    else:
        return None


def process_line(line, zx_log_processor: ZxLogProcessor):
    """
    Processa uma linha individual do log.

    Args:
        line (str): Linha do log
        zx_log_processor (ZxLogProcessor): Processador do arquivo ZxLog
    """
    clean_line = parse_log_line(line)
    if clean_line:
        command = check_command(clean_line)

        if command is not None:
            zx_log_processor.update_state(command)

        if zx_log_processor.is_game_saved:
            zx_log_processor.increase_lines_after_saving()
            print(
                f"Linhas lidas desde que houve um save = ${zx_log_processor.lines_after_saving}")

        if zx_log_processor.lines_after_saving == LINES_BETWEEN_SAVE_AND_START_SCREEN:
            zx_log_processor.process_save_event()


if __name__ == "__main__":
    read_tab_log(LOG_FILE_PATH)
