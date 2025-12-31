import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

from Command import Command


class ZxLogProcessor:
    def __init__(self, save_folder_path=None, max_backups=0, backup_prefix="Saves_Backup"):
        self.is_game_saved = False
        self.is_start_screen_loaded = False
        self.lines_after_saving = 0
        self.save_folder_path = self._setup_save_path(save_folder_path)
        # max_backups = 0 -> backups infinitos, não apaga os backups automaticamente
        self.max_backups = max_backups
        self.backup_prefix = backup_prefix

    def process_save_event(self):
        """Processa o evento de salvamento baseado no estado atual"""
        print("Processando evento de salvamento... ")
        print(f"is_start_screen_loaded = {self.is_start_screen_loaded}")
        if self.is_start_screen_loaded:
            print('Action executed - User manually saved')
            self.backup_save(is_manual_save=True)
        else:
            print('Action executed - Game autosaved')
            self.backup_save(is_manual_save=False)
        self.reset_state()

    def _setup_save_path(self, custom_path=None):
        """
        Configura o caminho da pasta de saves de forma multiplataforma.

        Args:
            custom_path: Caminho personalizado fornecido pelo usuário

        Returns:
            Path: Caminho da pasta de saves
        """
        if custom_path:
            return Path(custom_path)

        # Detecta o sistema operacional
        if sys.platform == "win32":
            # Windows - caminho padrão
            return Path.home() / "Documents" / "My Games" / "They Are Billions" / "Saves"
        elif sys.platform == "linux":
            # Linux - caminhos comuns para jogos
            linux_paths = [
                # Steam (Proton/SteamPlay)
                Path.home() / ".steam/steam/steamapps/compatdata/644930/pfx/drive_c/users/steamuser/Documents/My Games/They Are Billions/Saves",
                # Steam alternativa
                Path.home() / ".local/share/Steam/steamapps/compatdata/644930/pfx/drive_c/users/steamuser/Documents/My Games/They Are Billions/Saves",
                # Flatpak Steam
                Path.home() / ".var/app/com.valvesoftware.Steam/.steam/steam/steamapps/compatdata/644930/pfx/drive_c/users/steamuser/Documents/My Games/They Are Billions/Saves",
                # Local padrão do usuário
                Path.home() / ".local/share/they-are-billions/saves",
            ]

            # Tenta encontrar o primeiro caminho existente
            for path in linux_paths:
                if path.exists():
                    return path

            # Se nenhum existir, usa o mais provável
            return linux_paths[0]
        else:
            # macOS ou outros
            return Path.home() / "Documents" / "My Games" / "They Are Billions" / "Saves"

    def backup_save(self, is_manual_save: bool):
        """
        Copia a pasta de saves para um backup quando o usuário salva manualmente.
        """
        # Verifica se a pasta existe
        if not self.save_folder_path.exists():
            print(f"⚠️ Pasta de saves não encontrada: {self.save_folder_path}")
            return False

        try:
            # Cria um nome único com timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            new_folder_name = f"{self.backup_prefix}_manual_{timestamp}" if is_manual_save else f"{self.backup_prefix}_autosave_{timestamp}"

            # Caminho completo da nova pasta (mesmo diretório pai)
            backup_path = self.save_folder_path.parent / new_folder_name

            if backup_path.exists():
                print(f"Backup já existe: {backup_path.name}")
                return False

            # Copia recursivamente toda a pasta e seu conteúdo
            shutil.copytree(self.save_folder_path, backup_path)

            print(f"✅ Backup criado: {backup_path.name}")
            print(f"   Local: {backup_path}")

            # Opcional: Limitar número de backups
            if self.max_backups > 0:
                self.cleanup_old_backups()

            return True

        except PermissionError:
            print("✗ Erro de permissão. Feche o jogo antes de fazer backup.")
            return False
        except Exception as e:
            print(f"✗ Erro ao criar backup: {e}")
            return False

    def cleanup_old_backups(self):
        """
        Mantém apenas os últimos 'max_backups' e remove os mais antigos.

        """
        try:
            # Encontra todas as pastas de backup
            backup_folders = []
            for item in self.save_folder_path.parent.iterdir():
                if item.is_dir() and self.backup_prefix in item.name:
                    backup_folders.append(item)

            # Ordena por data de modificação (mais antigo primeiro)
            backup_folders.sort(key=os.path.getmtime)

            # Remove os mais antigos se exceder o limite
            while len(backup_folders) > self.max_backups:
                oldest = backup_folders.pop(0)
                shutil.rmtree(oldest)
                print(f"   Removido backup antigo: {oldest.name}")

        except Exception as e:
            print(f"   Nota: Não foi possível limpar backups antigos: {e}")

    def reset_state(self):
        """Reseta o estado para valores iniciais"""
        self.is_game_saved = False
        self.is_start_screen_loaded = False
        self.lines_after_saving = 0

    def update_state(self, command):
        """Atualiza o estado baseado no comando detectado"""
        if command == Command.SAVING_PROGRESS:
            print("Comando de salvar detectado")
            self.is_game_saved = True
            self.lines_after_saving = 0
        elif command == Command.LOADED_START_SCREEN:
            print("Comando de tela inicial carregada detectado")
            self.is_start_screen_loaded = True

    def increase_lines_after_saving(self):
        """ Incrementa o valor de linhas lidas após o jogo ter sido salvo """
        self.lines_after_saving += 1
