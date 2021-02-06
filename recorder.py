from dotenv import load_dotenv

load_dotenv()


def main(event, context):
    for record in event["Records"]:
        print(record)


if __name__ == "__main__":
    main({}, {})
