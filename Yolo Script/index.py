import argparse
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser(description="YOLO26 detection")
    parser.add_argument('--model', default='train/weights/best.pt', )
    parser.add_argument('--source', default='media/test.png')
    args = parser.parse_args()

    source = args.source.replace('usb', '') or '0' if args.source.startswith('usb') else args.source

    model = YOLO(args.model)

    for result in model.predict(source=source, show=True, stream=True, save=True, save_dir='output'):
        pass

if __name__ == "__main__":
    main()
