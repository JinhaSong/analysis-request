from Request.Request import Request
from utils import load_binary_image
import argparse
import os
import json

def parse_arguments():
    """Parse input arguments"""
    parser = argparse.ArgumentParser(description='Request generator')
    parser.add_argument("--url", dest='url', help='URL of analysis-site', type=str, default='http://mltwins.sogang.ac.kr:8777/analyzer/')
    parser.add_argument("--image_dir", dest='image_dir', help='Image dir to send as request', type=str, default=os.path.join(os.getcwd(), "images"))
    parser.add_argument("--result_dir", dest='result_dir', help='result dir to save', type=str, default=os.path.join(os.getcwd(), "result"))
    parser.add_argument("--modules", dest='modules', help='names of analysis-module', type=str, default="ssd-mobilenet-v2")

    return parser

if __name__ == '__main__':
    try :
        args = parse_arguments().parse_args()
        request = Request()

        image_dir = str(args.image_dir)
        result_dir = str(args.result_dir)

        image_list = os.listdir(image_dir)

        for image_name in image_list:
            image_path = os.path.join(image_dir, image_name)
            result_path = os.path.join(result_dir, image_name.split(".")[0] + ".json")
            b_image = load_binary_image(image_path)

            print("INFO: module={} / image_name={}\t======\t".format(args.modules, image_name), end="")
            request.set_request_attr(url=args.url, image_path=b_image, modules=args.modules)
            response = request.send_request_message()
            print("success\t======\t", end='')

            with open(result_path, 'w') as result_file :
                json.dump(response, result_file)
            print("saved", end='')

    except :
        print(" / fail")
