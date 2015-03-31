from ..cron import CronJob, CronTab, PurgeCronTab
import batou.vfs
import os.path
import pytest


def test_collects_cronjobs_into_crontab(root):
    root.environment.vfs_sandbox = batou.vfs.Developer(root.environment, None)
    root.component += CronJob('command1', timing='* * * * *')
    root.component += CronJob('command2', timing='* * * * *')
    root.component += CronTab()
    root.component.deploy()
    crontab = open(os.path.join(
        root.environment.workdir_base, 'mycomponent/crontab')).read()
    assert 'command1' in crontab
    assert 'command2' in crontab


def test_pruge_crontab_is_empty(root):
    root.environment.vfs_sandbox = batou.vfs.Developer(root.environment, None)
    root.component += PurgeCronTab()
    root.component.deploy()
    crontab = open(os.path.join(
        root.environment.workdir_base, 'mycomponent/crontab')).read()
    assert crontab == '# Generated by batou. Do not edit.\n\n\n'


def test_empty_crontab_must_raise(root):
    root.environment.vfs_sandbox = batou.vfs.Developer(root.environment, None)
    with pytest.raises(ValueError):
        root.component += CronTab()


def test_non_empty_pruge_crontab_must_raise(root):
    root.environment.vfs_sandbox = batou.vfs.Developer(root.environment, None)
    root.component += CronJob('command1', timing='* * * * *')
    root.component += CronJob('command2', timing='* * * * *')
    with pytest.raises(ValueError):
        root.component += CronTab(purge=True)
