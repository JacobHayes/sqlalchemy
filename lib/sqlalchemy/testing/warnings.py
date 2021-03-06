# testing/warnings.py
# Copyright (C) 2005-2020 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

from __future__ import absolute_import

import warnings

from . import assertions
from .. import exc as sa_exc


def setup_filters():
    """Set global warning behavior for the test suite."""

    warnings.filterwarnings(
        "ignore", category=sa_exc.SAPendingDeprecationWarning
    )
    warnings.filterwarnings("error", category=sa_exc.SADeprecationWarning)
    warnings.filterwarnings("error", category=sa_exc.SAWarning)

    # some selected deprecations...
    warnings.filterwarnings("error", category=DeprecationWarning)
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, message=".*StopIteration"
    )
    warnings.filterwarnings(
        "ignore", category=DeprecationWarning, message=".*inspect.get.*argspec"
    )

    # ignore things that are deprecated *as of* 2.0 :)
    warnings.filterwarnings(
        "ignore",
        category=sa_exc.SADeprecationWarning,
        message=r".*\(deprecated since: 2.0\)$",
    )
    warnings.filterwarnings(
        "ignore",
        category=sa_exc.SADeprecationWarning,
        message=r"^The (Sybase|firebird) dialect is deprecated and will be",
    )

    # 2.0 deprecation warnings, which we will want to have all of these
    # be "error" however for  I98b8defdf7c37b818b3824d02f7668e3f5f31c94
    # we are moving one at a time
    for msg in [
        #
        # Core execution
        #
        r"The (?:Executable|Engine)\.(?:execute|scalar)\(\) function",
        r"The current statement is being autocommitted using implicit "
        "autocommit,",
        r"The connection.execute\(\) method in SQLAlchemy 2.0 will accept "
        "parameters as a single dictionary or a single sequence of "
        "dictionaries only.",
        r"The Connection.connect\(\) function/method is considered legacy",
        r".*DefaultGenerator.execute\(\)",
        r"The autoload parameter is deprecated and will be removed ",
        #
        # result sets
        #
        r"The Row.keys\(\) function/method",
        r"Using non-integer/slice indices on Row ",
        #
        # Core SQL constructs
        #
        r"The FromClause\.select\(\).whereclause parameter is deprecated",
        r"Set functions such as union\(\), union_all\(\), extract\(\),",
        r"The legacy calling style of select\(\) is deprecated and will be "
        "removed",
        r"The FromClause.select\(\) method will no longer accept keyword "
        "arguments in version 2.0",
        r"The Join.select\(\) method will no longer accept keyword arguments "
        "in version 2.0.",
        r"The \"whens\" argument to case\(\) is now passed",
        r"The Join.select\(\).whereclause parameter is deprecated",
        #
        # DML
        #
        r"The (?:update|delete).whereclause parameter will be removed in "
        "SQLAlchemy 2.0.",
        r"The (?:insert|update).values parameter will be removed in "
        "SQLAlchemy 2.0.",
        r"The update.preserve_parameter_order parameter will be removed in "
        "SQLAlchemy 2.0.",
        r"Passing dialect keyword arguments directly to the "
        "(?:Insert|Update|Delete) constructor",
        #
        # ORM configuration
        #
        r"Calling the mapper\(\) function directly outside of a "
        "declarative registry",
        r"The ``declarative_base\(\)`` function is now available ",
        r"The ``has_inherited_table\(\)`` function is now available",
        r"The ``bind`` argument to declarative_base is deprecated and will "
        "be removed in SQLAlchemy 2.0.",
        #
        # ORM Query
        #
        r"The Query\.get\(\) function",
        r"The Query\.from_self\(\) function",
        r"The Query\.with_parent\(\) function",
        r"The Query\.with_parent\(\) function",
        r"The Query\.select_entity_from\(\) function",
        #
        # ORM Session
        #
        r"This Session located a target engine via bound metadata",
        r"The Session.autocommit parameter is deprecated ",
        r".*object is being merged into a Session along the backref "
        "cascade path",
        r"Passing bind arguments to Session.execute\(\) as keyword arguments",
        r"The Session.transaction function/method",
        r"The merge_result\(\) method is superseded by the "
        r"merge_frozen_result\(\)",
        r"The Session.begin.subtransactions flag is deprecated",
    ]:
        warnings.filterwarnings(
            "ignore", message=msg, category=sa_exc.RemovedIn20Warning,
        )

    try:
        import pytest
    except ImportError:
        pass
    else:
        warnings.filterwarnings(
            "once", category=pytest.PytestDeprecationWarning
        )


def assert_warnings(fn, warning_msgs, regex=False):
    """Assert that each of the given warnings are emitted by fn.

    Deprecated.  Please use assertions.expect_warnings().

    """

    with assertions._expect_warnings(
        sa_exc.SAWarning, warning_msgs, regex=regex
    ):
        return fn()
