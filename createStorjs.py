import os

iterations = 97
currentDir = os.getcwd()
runPortRangeStart = 1002
monitorPortRangeStart = runPortRangeStart+100

for i in range(iterations):
    print(runPortRangeStart+i)
    os.system(f'identity create storagenode{i} --concurrency 12')

for i in range(iterations):

    #os.system(f'identity create storagenode{i} --concurrency 12')
    #os.system(f"mkdir -p ~/.local/share/storj/identity/storagenode{i}/identity")

    identityToken = input(f'Inser identity Token for {i} node: ')
    os.system(f'identity authorize storagenode{i} {identityToken}')
        
    os.system(f'mkdir {currentDir}/{runPortRangeStart+i} && \
        mkdir {currentDir}/{runPortRangeStart+i}/identity && \
        mv ~/.local/share/storj/identity/storagenode{i}/* {currentDir}/{runPortRangeStart+i}/identity && \
        mkdir {currentDir}/{runPortRangeStart+i}/scripts && \
        mkdir {currentDir}/{runPortRangeStart+i}/storage')

    setupScript = f'docker run --rm -e SETUP="true" \
        --user $(id -u):$(id -g) \
        --mount type=bind,source="{currentDir}/{runPortRangeStart+i}/identity",destination=/app/identity \
        --mount type=bind,source="{currentDir}/{runPortRangeStart+i}/storage",destination=/app/config \
        --name storagenode{runPortRangeStart+i} storjlabs/storagenode:latest'
    
    setupScriptFile = open(f"{currentDir}/{runPortRangeStart+i}/scripts/setupScript.sh", "w")  # write mode
    setupScriptFile.write(setupScript)
    setupScriptFile.close()

    runScript =  f'docker run -d --restart unless-stopped --stop-timeout 300 \
        -p {runPortRangeStart+i}:28967/tcp \
        -p {runPortRangeStart+i}:28967/udp \
        -p 127.0.0.1:{monitorPortRangeStart+i}:14002 \
        -e WALLET="0x7f532f04bf17bdefc4d1093ff5ae24efff39c6cf" \
        -e EMAIL="filip.bobek13@gmail.com" \
        -e ADDRESS="212.5.194.56:{runPortRangeStart+i}" \
        -e STORAGE="2TB" \
        --user $(id -u):$(id -g) \
        --mount type=bind,source="{currentDir}/{runPortRangeStart+i}/identity",destination=/app/identity \
        --mount type=bind,source="{currentDir}/{runPortRangeStart+i}/storage",destination=/app/config \
        --name storagenode{runPortRangeStart+i} storjlabs/storagenode:latest'
        
    runScriptFile = open(f"{currentDir}/{runPortRangeStart+i}/scripts/runScript.sh", "w")  # write mode
    runScriptFile.write(runScript)
    runScriptFile.close()

    watchScript =  f'docker run -d --restart=always --name watchtower{runPortRangeStart+i} \
        -v /var/run/docker.sock:/var/run/docker.sock storjlabs/watchtower \
        storagenode{runPortRangeStart+i} watchtower{runPortRangeStart+i} --stop-timeout 300s'
    
    watchScriptFile = open(f"{currentDir}/{runPortRangeStart+i}/scripts/watchScript.sh", "w")  # write mode
    watchScriptFile.write(watchScript)
    watchScriptFile.close()

    os.system(f'bash {currentDir}/{runPortRangeStart+i}/scripts/setupScript.sh')
    os.system(f'bash {currentDir}/{runPortRangeStart+i}/scripts/runScript.sh')
    os.system(f'bash {currentDir}/{runPortRangeStart+i}/scripts/watchScript.sh')


print()