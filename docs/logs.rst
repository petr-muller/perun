.. _logs-overview:

Customize Logs and Statuses
===========================

``log`` and ``status`` commands print information about wrapped repository annotated by performance
profiles. ``perun log`` command lists the minor versions history for a major version (currently the
checked out), along with the information about registered profiles, such as e.g. the minor version
description, authors, statistics of profiles, etc. ``perun status`` commands shows the overview of
given minor version of current major head and lists profiles associated to profiles and in pending
directory (i.e. the ``.perun/jobs`` directory. List of profiles contains the types of profiles,
numbers, configurations of profiling run, etc.

The format of outputs of both ``log`` and ``status`` can be customized by setting the formatting
strings c.f. :ref:`logs-log` and :ref:`logs-status`. Moreover, outputs are paged (currently using
the ``less -R`` command) by default. To turn off the paging, run the ``perun`` with ``--no-pager``
option (see :doc:`cli`) or set :ckey:`global.paging`.

.. _logs-status:

Customizing Statuses
--------------------

The output of ``perun status`` is defined w.r.t. formatting string specified in configuration in
:ckey:`global.profile_info_fmt` key (looked up recursively in the nearest local configuration, or
in global configuration). The formatting string consists of raw delimiters and special tags, which
serves as templates to output specific informations about concrete profiles, such as the profiling
configuration, type of profile, creating timestamps, etc.

E.g. the following formatting string::

     ┃ [type] ┃ [cmd] ┃ [workload] ┃ [collector]  ┃ ([time]) ┃

will yield the following status when running ``perun status`` (both for stored and pending
profiles)::

    ═══════════════════════════════════════════════════════════════════════════════▣
      id ┃   type  ┃  cmd   ┃ workload ┃  args  ┃ collector  ┃         time        ┃
    ═══════════════════════════════════════════════════════════════════════════════▣
     0@p ┃ [mixed] ┃ target ┃ hello    ┃        ┃ complexity ┃ 2017-09-07 14:41:49 ┃
     1@p ┃ [time ] ┃ perun  ┃          ┃ status ┃ time       ┃ 2017-10-19 12:30:29 ┃
     2@p ┃ [time ] ┃ perun  ┃          ┃ --help ┃ time       ┃ 2017-10-19 12:30:31 ┃
    ═══════════════════════════════════════════════════════════════════════════════▣

The first column of the ``perun status`` output, ``id``, has a fixed position and defines a tag for
the given, which can be used in ``add``, ``rm``, ``show`` and ``postprocessby`` commands as a quick
wildcard for concrete profiles, e.g. ``perun add 0@p`` would register the first profile stored in
the pending ``.perun/jobs`` directory to the index of current head. Tags are always in form of
``i@p`` (for pending profiles) and ``i@i`` for profiles registered in index, where ``i`` stands for
position in the corresponding storage, index from zero. 

The specification of the formatting string can contain the following special tags:

``[type]``:
    Lists the most generic type of the profile according to the collected resources serving as
    quick tagging of similar profiles. Currently Perun supports `memory`, `time`, `mixed`.

``[cmd]``:
    Lists the command for which the data was collected, this e.g. corresponds to the binary or
    script that was executed and profiled using collector/profiler. Refer to :ref:`jobs-overview`
    for more information about profiling jobs and commands.

``[args]``:
    Lists the arguments (or parameters) which were passed to the profiled command. Refer to
    :ref:`jobs-overview` for more information about profiling jobs and command arguments.

``[workload]``:
    List input workload which was passed to the profiled command, i.e. some inputs of the profiled
    program, script or binary. Refer to :ref:`jobs-overview` for more information about profiling
    jobs and command workloads.

``[collector]``:
    Lists the collector which was used to obtain the given profile. Refer to :doc:`collectors` for
    list of supported collectors and more information about collection of profiles.

``[time]``:
    Timestamp when the profile was last modified in format `YEAR-MONTH-DAY HOURS:MINUTES:SECONDS`.

``[id]``:
    Original identification of the profile. This corresponds to the name of the generated profile
    and the original path.

.. _logs-log:

Customizing Logs
----------------

.. todo:: 
    FFS, this is not even currently working in Perun. ^\(-_-)/^

The output of ``perun log --short`` is defined w.r.t. formatting string specified in configuration
in :ckey:`global.minor_version_info_fmt` key (looked up recursively in the nearest local
configuration, or in global configuration). The formatting string can contain both raw characters
(such as delimiters, etc.) and special tags, which serves as templates to output information for
concrete minor version such as minor version description, number of assigned profiles, etc.

E.g. the following formatting string::

    '[id:6] ([stats]) [desc]'

will yield the following output when running ``perun log --short``::

    minor   (a|m|x|t profiles) info
    53d35c  (2|0|2|0 profiles) Add deleted jobs directory
    07f2b4  (1|0|1|0 profiles) Add necessary files for perun to work on this repo.
    bd3dc3  ---no--profiles--- root


The specification of the formatting string can contain the following special tags:

``[id:num]``:
    Identification of the minor version (should be hash preferably). If we take ``git`` as an
    example ``id`` will correspond to the SHA of one commit. Specifying ``num`` in the template
    will shorten the displayed identification to ``num`` characters.

``[stats]``:
    Lists short summary of overall number of profiles (``a``) and number of memory (``m``), mixed
    (``x``) and time (``t``) profiles assinged to given minor version.

``[desc]``:
    Lists short description of the minor version. If we take ``git`` as an example this will
    correspond to the short commit message.

``[date]``:
    Lists the date the minor version was commited (in the wrapped vcs).

``[author]``:
    Lists the author of the minor version (not commiter).

``[email]``:
    Lists the email of the author of the minor version.

``[parents]``:
    Lists the parents of the given minor version. Note that one minor version can have potentially
    several parents, e.g. in git, when the merge of two commits happens.
