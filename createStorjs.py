import os

iterations = 10
currentDir = os.getcwd()

for i in range(iterations):

    os.system(f'mkdir ~/.local/share/storj/identity && \
        mkdir {currentDir}/{i} && \
        mv ~/.local/share/storj/* {currentDir}/{i} && \
        mkdir {currentDir}/{i}/scripts && \
        mkdir {currentDir}/{i}/storagenode')

    setupScript = f'sudo docker run --rm -e SETUP="true" \
        --user $(id -u):$(id -g) \
        --mount type=bind,source="{currentDir}/{i}/identity",destination=/app/identity \
        --mount type=bind,source="{currentDir}/{i}/storagenode",destination=/app/config \
        --name storagenode storjlabs/storagenode:latest'
    
    setupScriptFile = open(f"{currentDir}/{i}/scripts/setupScript", "w")  # write mode
    setupScriptFile.write(setupScript)
    setupScriptFile.close()


print()