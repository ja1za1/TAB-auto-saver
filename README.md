# TAB Auto Saver

Um programa em Python que monitora automaticamente os arquivos de log do jogo **They Are Billions (TAB)** para detectar quando um salvamento acontece e criar backups automáticos dos arquivos de save.

## 📋 Descrição

O TAB Auto Saver lê continuamente o arquivo de log do jogo (`ZXLog.txt`) e identifica quando ocorre um salvamento. O programa diferencia entre:

- **Salvamento Manual**: Quando o jogador salva o jogo manualmente
- **Salvamento Automático**: Quando o jogo salva automaticamente

Quando um salvamento é detectado, o programa cria automaticamente um backup completo da pasta de saves do jogo, organizando os backups com timestamps e identificando se foram salvamentos manuais ou automáticos.

## 🚀 Como Usar

### 1. Configuração do Ambiente Virtual

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

### 2. Instalação de Dependências

```bash
pip install -r requirements.txt
```

**Nota**: Este projeto utiliza apenas bibliotecas padrão do Python, então não há dependências externas necessárias.

### 3. Configuração

Antes de executar, você precisa editar o arquivo `main.py` e ajustar os seguintes caminhos conforme sua instalação do jogo:

- `LOG_FILE_PATH`: Caminho para o arquivo `ZXLog.txt` do jogo
- `SAVES_FOLDER`: Caminho para a pasta de saves do jogo

### 4. Execução

```bash
python main.py
```

O programa começará a monitorar o arquivo de log. Pressione `Ctrl+C` para encerrar o programa.

## 📁 Estrutura do Projeto

```
TAB-auto-saver/
├── venv/                 # Ambiente virtual Python
├── main.py              # Arquivo principal - monitora o log
├── ZxLogProcessor.py    # Processador de log e gerenciador de backups
├── command.py           # Definições de comandos/enums
├── requirements.txt     # Dependências do projeto
└── README.md           # Este arquivo
```

## 🔧 Funcionalidades

- **Monitoramento em Tempo Real**: Lê o arquivo de log continuamente
- **Detecção de Salvamentos**: Identifica quando o jogo salva (manual ou automático)
- **Backups Automáticos**: Cria backups completos da pasta de saves
- **Organização de Backups**: Nomeia os backups com timestamps e tipo de salvamento
- **Limpeza Automática**: Opção para manter apenas os últimos N backups (configurável)
- **Multiplataforma**: Suporta Windows, Linux e macOS

## ⚙️ Configurações

No arquivo `main.py`, você pode ajustar:

- `LINES_BETWEEN_SAVE_AND_START_SCREEN`: Número de linhas entre o salvamento e a tela inicial (padrão: 25)
- `max_backups`: Número máximo de backups a manter (0 = infinitos, padrão: 5)

## 📝 Como Funciona

1. O programa monitora o arquivo `ZXLog.txt` em tempo real
2. Quando detecta a mensagem "Salvando progresso", marca que um salvamento ocorreu
3. Se detecta "Load Success" na tela inicial antes do salvamento, identifica como salvamento manual
4. Após ler um número específico de linhas após o salvamento, cria o backup
5. Os backups são salvos na mesma pasta pai da pasta de saves, com nomes como:
   - `Saves_Backup_manual_2024-01-15_14-30-45`
   - `Saves_Backup_autosave_2024-01-15_14-30-45`

## ⚠️ Observações

- Certifique-se de que o jogo não está em execução ao criar backups, para evitar erros de permissão
- O programa precisa ter permissões de leitura no arquivo de log e de escrita na pasta de saves
- Os caminhos padrão são detectados automaticamente, mas podem ser configurados manualmente

## 📄 Licença

Este projeto é de código aberto e está disponível para uso pessoal.

