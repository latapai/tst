### How to install

There are 2 options to run this environment chose the one that is most appropriated for you.

#### Option 1
1. Download the VSCode extension: Dev containers
2. Open the command palette (Ctrl+Shift+P) and select: Remote-Containers: Rebuid and Reopen in Container
3. Once you're running in the dev container, open a terminal (within VSCode, thus running inside the container) and run the following command:

  `pip install "ibm-bampy[langchain]" --extra-index-url https://na.artifactory.swg-devops.com/artifactory/api/pypi/res-bampy-team-pypi-local/simple --upgrade`

5. Use your IBM credentials and answer "no" (N) to the question
6. Run the application by typing in the terminal: "streamlit run app/main.py"

#### Option 2
1. Clone the repository
2. Build a docker container using provided Docker file:

`docker build -t wx-demo-car-insurance . `

3. Get your BAM keys from https://bam.res.ibm.com/ 
4. Start the docker container:

`docker run -e FMAAS_MODEL_ID=google/flan-ul2 -e BAM_API_KEY=<your-BAM-key> -e FMAAS_API_KEY=1 -p 8080:8080 wx-demo-car-insurance`

5. Use your prefered browser and navigate to http://localhost:8080 


NOTE: To connect with WatsonxX Internal (BAM) you need VPN accees from your own system, otherwise the API FQD will not be resolved. 
