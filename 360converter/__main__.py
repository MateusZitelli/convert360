import imageio
import argparse
from projector import get_projector


def render_video(renderer, reader, writer):
    for i, frame in enumerate(reader):
        img = renderer.render_to_image(frame)
        writer.append_data(img)


def render_image(renderer, reader, writer):
    frame = reader.get_data(0)
    img = renderer.render_to_image(frame)
    writer.append_data(img)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description= 'Cube-map to equiretangular \
                                     conversor.')
    parser.add_argument('-i', '--input', type=str, required=True,
                        metavar='FILE', dest='input',
                        help='Equiretangular video to be converted.')
    parser.add_argument('-o', '--output', type=str, required=True,
                        metavar='FILE', dest='output',
                        help='Output cube-map video.')
    parser.add_argument('-s', '--size', type=int, default=[512, 512],
                        nargs=2, metavar=('WIDTH', 'HEIGHT'), dest='size',
                        help='Cube faces size in pixels.')
    parser.add_argument('-it', '--input-type', type=str,
                        default='equirectangular', choices=['equirectangular'],
                        metavar='TYPE', dest='input_type',
                        help='Cube faces size in pixels.')
    parser.add_argument('-ot', '--output-type', type=str,
                        default='cubemap', choices=['cubemap'],
                        metavar='TYPE', dest='output_type',
                        help='Cube faces size in pixels.')
    args = parser.parse_args()
    output_size = (args.size[0] * 3, args.size[1] * 2)

    reader = imageio.get_reader(args.input)
    metadata = reader.get_meta_data()

    projector = get_projector(args.input_type, args.output_type)

    with projector(output_size) as renderer:
        writer_args = {}
        if 'fps' in metadata:
            # Handle videos
            writer_args['fps'] = metadata['fps']

        with imageio.get_writer(args.output, **writer_args) as writer:
            render_video(renderer, reader, writer)
