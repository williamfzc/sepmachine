FROM williamfzc/stagesepx

RUN apt update && \
    apt install scrcpy && \
    apt clean
