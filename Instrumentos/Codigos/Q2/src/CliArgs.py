import argparse


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--cursor', help='Initial cursor string', default=None)
    parser.add_argument(
        '--total', help='Total repos to be fetch', default=1000)
    parser.add_argument(
        '--per-request', help='Number of repos per request', default=100)

    return parser.parse_args()
