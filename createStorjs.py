import os

iterations = 1
currentDir = os.getcwd()
runPortRangeStart = 1000
monitorPortRangeStart = 1100

for i in range(iterations):

    os.system(f'identity create storagenode{i}')
    #os.system(f"mkdir -p ~/.local/share/storj/identity/storagenode{i}/identity")

    identityToken = input(f'Inser identity Token for {i} node: ')
    os.system(f'identity authorize storagenode{i} {identityToken}')
    print(identityToken)
    
    os.system(f'mkdir {currentDir}/{runPortRangeStart+i} && \
        mv ~/.local/share/storj/identity/storagenode{i}/* {currentDir}/{runPortRangeStart+i}/identity && \
        mkdir {currentDir}/{runPortRangeStart+i}/scripts && \
        mkdir {currentDir}/{runPortRangeStart+i}/storage')

    setupScript = f'docker run --rm -e SETUP="true" \
        --user $(id -u):$(id -g) \
        --mount type=bind,source="{currentDir}/{runPortRangeStart+i}/identity",destination=/app/identity \
        --mount type=bind,source="{currentDir}/{runPortRangeStart+i}/storage",destination=/app/config \
        --name storagenode{i} storjlabs/storagenode:latest'
    
    setupScriptFile = open(f"{currentDir}/{runPortRangeStart+i}/scripts/setupScript.sh", "w")  # write mode
    setupScriptFile.write(setupScript)
    setupScriptFile.close()

    runScript =  f'docker run -d --restart unless-stopped --stop-timeout 300 \
        -p {runPortRangeStart+i}:{runPortRangeStart+i}/tcp \
        -p {runPortRangeStart+i}:{runPortRangeStart+i}/udp \
        -p 127.0.0.1:{monitorPortRangeStart+i}:{monitorPortRangeStart+i} \
        -e WALLET="0x7f532f04bf17bdefc4d1093ff5ae24efff39c6cf" \
        -e EMAIL="filip.bobek13@gmail.com" \
        -e ADDRESS="212.5.194.56:{runPortRangeStart+i}" \
        -e STORAGE="2TB" \
        --user $(id -u):$(id -g) \
        --mount type=bind,source="{currentDir}/{runPortRangeStart+i}/identity",destination=/app/identity \
        --mount type=bind,source="{currentDir}/{runPortRangeStart+i}/storage",destination=/app/config \
        --name storagenode{i} storjlabs/storagenode:latest'
        
    runScriptFile = open(f"{currentDir}/{runPortRangeStart+i}/scripts/runScript.sh", "w")  # write mode
    runScriptFile.write(runScript)
    runScriptFile.close()

    watchScript =  f'docker run -d --restart=always --name watchtower{i} \
        -v /var/run/docker.sock:/var/run/docker.sock storjlabs/watchtower \
        storagenode{i} watchtower{i} --stop-timeout 300s'
    
    watchScriptFile = open(f"{currentDir}/{runPortRangeStart+i}/scripts/watchScript.sh", "w")  # write mode
    watchScriptFile.write(watchScript)
    watchScriptFile.close()

    os.system(f'bash {currentDir}/{runPortRangeStart+i}/scripts/setupScript.sh')
    os.system(f'bash {currentDir}/{runPortRangeStart+i}/scripts/runScript.sh')
    os.system(f'bash {currentDir}/{runPortRangeStart+i}/scripts/watchScript.sh')


print()