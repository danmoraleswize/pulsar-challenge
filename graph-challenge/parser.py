from lxml import etree
import traceback
import click
import os
base_path = os.path.dirname(os.path.realpath('__file__'))


def xml_to_rdf(source, stylesheet):
    # Parsing management signals
    stylesheet_path = os.path.join(base_path, stylesheet)
    # print("XSLT_PATH", stylesheet_path)
    xslt_root = etree.parse(stylesheet_path)
    transform = etree.XSLT(xslt_root)

    # Load the source and apply the transform
    file_path = os.path.join(base_path, source)
    # print("FILE_PATH", file_path)
    tree = etree.parse(file_path)
    result_tree = transform(tree)
    return result_tree


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option(
    '-i', '--input-file',
    help="""XML source format file.""",
    type=str,
    required=True
)
@click.option(
    '-o', '--output-file',
    help="""XML output file.""",
    type=str,
    required=True
)
@click.option(
    '-p', '--parser',
    help="""XSLT transformation stylesheet.""",
    type=str,
    required=True
)
def _smoke_test(input_file=None, output_file=None, parser=None):
    if input_file and output_file and parser:
        try:
            rdf_object = xml_to_rdf(input_file, parser)
            out_path = base_path + '/output/' + output_file
            # print("OUT_PATH", out_path)
            rdf_object.write(out_path)
            print(f"[OK]  -  RDF Object ready under {out_path}")
        except Exception as err:
            print('[ERROR]', traceback.format_exc())
            print(f"[ERROR]  -  Something went wrong please verify sources")


if __name__ == '__main__':
    _smoke_test()
