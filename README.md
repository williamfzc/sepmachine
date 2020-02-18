# sepmachine

stagesepx + video capture = auto workflow

## global

wrapper of stagesepx, for convenient usage.

## structure

### modules

- (video) capture
    - different platforms
        - android
        - ios
        - external camera
        - ...
    - (record and) return a video path to handler
- (video) handler
    - with (or without) trained models
    - hook functions for custom actions
- pipeline
    - bind capture and handler together, and make them work
    - loop

## license

[MIT](LICENSE)
