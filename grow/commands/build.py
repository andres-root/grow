"""Command for building pods into static deployments."""

import os
import click
from grow.common import utils
from grow.deployments import stats
from grow.deployments.destinations import local as local_destination
from grow.pods import pods
from grow.pods import storage
from grow.performance import profile_report


# pylint: disable=too-many-locals
@click.command()
@click.argument('pod_path', default='.')
@click.option('--out_dir', help='Where to output built files.')
@click.option('--preprocess/--no-preprocess', '-p/-np',
              default=True, is_flag=True,
              help='Whether to run preprocessors.')
@click.option('--clear_cache',
              default=False, is_flag=True,
              help='Clear the pod cache before building.')
@click.option('--file', '--pod-path', 'pod_paths',
              help='Build only pages affected by content files.', multiple=True)
@click.option('--locate-untranslated',
              default=False, is_flag=True,
              help='Shows untranslated message information.')
@click.option('--profile',
              default=False, is_flag=True,
              help='Show report of pod operation timing for performance analysis.')
def build(pod_path, out_dir, preprocess, clear_cache, pod_paths, locate_untranslated, profile):
    """Generates static files and dumps them to a local destination."""
    root = os.path.abspath(os.path.join(os.getcwd(), pod_path))
    out_dir = out_dir or os.path.join(root, 'build')
    pod = pods.Pod(root, storage=storage.FileStorage)
    if clear_cache:
        pod.podcache.reset(force=True)
    if preprocess:
        pod.preprocess()
    if locate_untranslated:
        pod.enable(pod.FEATURE_TRANSLATION_STATS)
    try:
        config = local_destination.Config(out_dir=out_dir)
        destination = local_destination.LocalDestination(config)
        destination.pod = pod
        paths, _ = pod.determine_paths_to_build(pod_paths=pod_paths)
        repo = utils.get_git_repo(pod.root)
        stats_obj = stats.Stats(pod, paths=paths)
        content_generator = destination.dump(pod, pod_paths=pod_paths)
        destination.deploy(content_generator, stats=stats_obj, repo=repo, confirm=False,
                           test=False, is_partial=bool(pod_paths))
        pod.podcache.write()
    except pods.Error as err:
        raise click.ClickException(str(err))
    if locate_untranslated:
        pod.translation_stats.pretty_print()
        destination.export_untranslated_catalogs()
    if profile:
        report = profile_report.ProfileReport(pod.profile)
        report.pretty_print()
        destination.export_profile_report()
