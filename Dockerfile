### builder
FROM openjdk:8 AS builder

RUN apt update && apt install -y ffmpeg libsdl2-2.0-0 android-tools-adb

# client build dependencies
RUN apt install -y gcc git pkg-config meson ninja-build \
                 libavcodec-dev libavformat-dev libavutil-dev \
                 libsdl2-dev

ARG SCRCPY_VER=1.12.1
ARG SERVER_HASH="63e569c8a1d0c1df31d48c4214871c479a601782945fed50c1e61167d78266ea"

RUN curl -L -o scrcpy-server https://github.com/Genymobile/scrcpy/releases/download/v${SCRCPY_VER}/scrcpy-server-v${SCRCPY_VER} && \
    echo "$SERVER_HASH  /scrcpy-server" | sha256sum -c -
RUN git clone --branch v${SCRCPY_VER} --depth 1 https://github.com/Genymobile/scrcpy.git
RUN cd scrcpy && meson x --buildtype release --strip -Db_lto=true -Dprebuilt_server=/scrcpy-server && ninja -Cx install

### runner
FROM williamfzc/stagesepx AS runner

COPY --from=builder /usr/local/share/scrcpy/scrcpy-server /usr/local/share/scrcpy/scrcpy-server
COPY --from=builder /usr/local/bin/scrcpy /usr/local/bin/scrcpy

RUN apt-get update && \
    apt-get install -y android-tools-adb git && \
    apt-get clean
