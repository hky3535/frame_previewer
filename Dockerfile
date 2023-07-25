FROM ubuntu:latest

COPY . /workspace/frame_previewer

WORKDIR /workspace/frame_previewer
CMD ["sh", "run.sh"]