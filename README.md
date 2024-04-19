# RANIA HUB

To run this app, ensure you have node installed and up to date on your machine. Additionally, ensure the appropriate .env variables are defined.
After node is installed, run npm install to add the node packages and then run the command npm start to run the application.

# RANIA LLM Smart Home Assistant

Assistant is located in `WVU-RANIA-Dashboard/SmartHomeAssistant` which contains `web/` (React app) and `assistant/` (Python backend)

## First time setup

> [!IMPORTANT]  
> Requires Linux or a UNIX-based OS. If you are running Windows, either use a VM or use WSL.

1. Initialize Python virtual environment once you are located in the `WVU-RANIA-Dashboard/SmartHomeAssistant`

```bash
python -m venv ./.venv/
```

2. Activate virtual environment

```bash
source /path/to/.venv/bin/activate
```

3. Install required packages

```bash
pip install -r requirements.txt
pip3 install -r requirements.txt
```

4. Navigate to `SmartHomeAssistant/web/`

5. Install npm packages

```bash
npm install
```

6. Navigate to `SmartHomeAssistant/whisper.cpp/`

7. Run `make`

8. Navigate to `SmartHomeAssistant/whisper.cpp/models/`

9. Run `./download-ggml-model.sh tiny.en-q5_1.bin` or a different model if applicable

## How to use

1. Activate virtual environment with `source .venv/bin/activate`

2. Run `python3 main.py` located in `assistant/`

3. Run `npm start` located in `web/`
