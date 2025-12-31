# TAB Auto Saver

Um programa em Python que monitora automaticamente os arquivos de log do jogo **They Are Billions (TAB)** para detectar quando um salvamento acontece e criar backups automáticos dos arquivos de save.

## 📋 Descrição

O TAB Auto Saver lê continuamente o arquivo de log do jogo (`ZXLog.txt`) e identifica quando ocorre um salvamento. O programa diferencia entre:

- **Salvamento Manual**: Quando o jogador salva o jogo manualmente
- **Salvamento Automático**: Quando o jogo salva automaticamente

Quando um salvamento é detectado, o programa cria automaticamente um backup completo da pasta de saves do jogo, organizando os backups com timestamps e identificando se foram salvamentos manuais ou automáticos.

## 🚀 Como Usar

### 1. Configuração

Antes de executar, você precisa editar o arquivo `main.py` e ajustar as seguintes constantes conforme sua instalação do jogo:

#### Constantes Obrigatórias:

- **`LOG_FILE_PATH`**: Caminho completo para o arquivo `ZXLog.txt` do jogo. Geralmente está localizado na mesma pasta onde a pasta de saves está localizada.

  ```python
  LOG_FILE_PATH = "C:\\Users\\SeuUsuario\\Documents\\My Games\\They Are Billions\\ZXLog.txt"
  ```

- **`SAVES_FOLDER`**: Caminho completo para a pasta de saves do jogo.
  ```python
  SAVES_FOLDER = "C:\\Users\\SeuUsuario\\Documents\\My Games\\They Are Billions\\Saves"
  ```

#### Constantes Opcionais:

- **`LINES_BETWEEN_SAVE_AND_START_SCREEN`**: Número de linhas que o programa deve ler após detectar um salvamento antes de processar o evento. Este valor é crítico para o funcionamento correto do programa e **não deve ser alterado** a menos que você saiba o que está fazendo. Valor padrão: `25`

- **`MAX_BACKUPS`**: Número máximo de backups que o programa pode criar. Quando esse limite é atingido, o backup mais antigo é automaticamente removido para dar espaço ao novo. Se definido como `0`, o programa manterá todos os backups indefinidamente (sem limpeza automática). Valor padrão: `5`

- **`BACKUP_PREFIX`**: Prefixo usado para nomear as pastas de backup criadas. Os backups serão nomeados como `{BACKUP_PREFIX}_manual_{timestamp}` ou `{BACKUP_PREFIX}_autosave_{timestamp}`. Valor padrão: `"Saves_Backup"`

### 2. Execução

```bash
python main.py
```

O programa começará a monitorar o arquivo de log. Pressione `Ctrl+C` para encerrar o programa.

## 📁 Estrutura do Projeto

```
TAB-auto-saver/
├── main.py              # Arquivo principal - monitora o log e configurações
├── ZxLogProcessor.py    # Processador de log e gerenciador de backups
├── command.py           # Definições de comandos/enums
└── README.md           # Este arquivo
```

## 🔧 Funcionalidades

- **Monitoramento em Tempo Real**: Lê o arquivo de log continuamente
- **Detecção de Salvamentos**: Identifica quando o jogo salva (manual ou automático)
- **Backups Automáticos**: Cria backups completos da pasta de saves
- **Organização de Backups**: Nomeia os backups com timestamps e tipo de salvamento
- **Limpeza Automática**: Opção para manter apenas os últimos N backups (configurável via `MAX_BACKUPS`)
- **Multiplataforma**: Suporta Windows, Linux e macOS

## 📝 Como Funciona

1. O programa monitora o arquivo `ZXLog.txt` em tempo real
2. Quando detecta a mensagem "Salvando progresso", marca que um salvamento ocorreu
3. Se detecta "Load Success" na tela inicial antes do salvamento, identifica como salvamento manual
4. Após ler um número específico de linhas após o salvamento (definido por `LINES_BETWEEN_SAVE_AND_START_SCREEN`), cria o backup
5. Os backups são salvos na mesma pasta pai da pasta de saves, com nomes como:
   - `Saves_Backup_manual_2024-01-15_14-30-45`
   - `Saves_Backup_autosave_2024-01-15_14-30-45`

## ⚙️ Resumo das Constantes

| Constante                             | Tipo        | Descrição                    | Valor Padrão         |
| ------------------------------------- | ----------- | ---------------------------- | -------------------- |
| `LOG_FILE_PATH`                       | Obrigatória | Caminho do arquivo ZXLog.txt | Deve ser configurado |
| `SAVES_FOLDER`                        | Obrigatória | Caminho da pasta de saves    | Deve ser configurado |
| `LINES_BETWEEN_SAVE_AND_START_SCREEN` | Opcional    | Linhas a ler após salvamento | `25` (não alterar)   |
| `MAX_BACKUPS`                         | Opcional    | Máximo de backups a manter   | `5` (0 = infinitos)  |
| `BACKUP_PREFIX`                       | Opcional    | Prefixo dos nomes de backup  | `"Saves_Backup"`     |

## ⚠️ Observações

- O programa deve ser executado APÓS o jogo estar aberto
- O programa precisa ter permissões de leitura no arquivo de log e de escrita na pasta de saves
- Se `MAX_BACKUPS` for definido como `0`, todos os backups serão mantidos indefinidamente

## 📄 Licença

Este projeto é de código aberto e está disponível para uso pessoal.
