# RANIA HUB

To run this app, ensure you have node installed and up to date on your machine. Additionally, ensure the appropriate .env variables are defined.
After node is installed, run npm install to add the node packages and then run the command npm start to run the application.

# RANIA LLM Smart Home Assistant

Assistant is located in `WVU-RANIA-Dashboard/SmartHomeAssistant` which contains `web/` (React app) and `assistant/` (Python backend)

## First time setup

> [!IMPORTANT]  
> Requires Linux or a UNIX-based OS. If you are running Windows, either use a VM or use WSL.
> Tested on Debian-based distros (Ubuntu, Raspberry Pi OS).
> Debian-based distros are **HIGHLY RECOMMENDED**

1. Install [Miniforge3](https://github.com/conda-forge/miniforge)
2. Install OpenBLAS and dependencies for Whisper.cpp
```bash
sudo apt-get install g++ cmake libopenblas-dev
```
3. Configure conda environment
```bash
conda env create -f environment.yaml
```
> [!NOTE]
> If running on an ARM CPU, run `conda env create -f armenv.yaml` instead

4. Activate conda environment
```bash
conda activate rania
```
> [!IMPORTANT]  
> PyAudio and PocketSphinx require portaudio19-dev, pulseaudio, swig, and libpulse-dev to work properly
```bash
sudo apt install portaudio19-dev pulseaudio swig libpulse-dev
```

4. Navigate to `SmartHomeAssistant/web/`

5. Install npm packages

```bash
npm install
```

6. Navigate to `SmartHomeAssistant/whisper.cpp/`

7. Compile whisper.cpp with [OpenBLAS](https://github.com/ggerganov/whisper.cpp?tab=readme-ov-file#blas-cpu-support-via-openblas)
```bash
make clean
WHISPER_OPENBLAS=1 make -j
```
8. Navigate to `SmartHomeAssistant/whisper.cpp/models/`

9. Run `./download-ggml-model.sh tiny.en-q5_1.bin` or a different model if applicable

## How to use

1. Activate virtual environment with `conda activate rania`

2. Run `python3 main.py` located in `assistant/`

3. Run `npm start` located in `web/`
