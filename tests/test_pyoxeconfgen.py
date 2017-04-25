#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from click.testing import CliRunner

from pyoxeconfgen.__main__ import main


def test_main():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.output == 'Pyoxeconfgen main command line invoked.\n'
    assert result.exit_code == 0
