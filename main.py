from utils import get_data


def main():
    OPERATIONS_URL = "https://s3.us-west-2.amazonaws.com/secure.notion-static.com/d22c7143-d55e-4f1d-aa98-e9b15e5e5efc/operations.json?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=AKIAT73L2G45EIPT3X45%2F20230206%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20230206T162548Z&X-Amz-Expires=86400&X-Amz-Signature=e448201bfff190c1151811f1f2651403cdbce7f2fd9b5bc677d482dfc8e5b12c&X-Amz-SignedHeaders=host&response-content-disposition=filename%3D%22operations.json%22&x-id=GetObject"
    data, info = get_data(OPERATIONS_URL)
    if not data:                # data are not received
        exit(info)
    else:
        print(info)

if __name__ == "__main__":
    main()
