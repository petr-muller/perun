Changelog
=========

HEAD
----

**To be included in next release**

  - add global.paging option (see :ckey:`general.paging`)
  - improve bokeh outputs (with click policy, and better lines)

0.11 (2017-11-27)
-----------------

**Adding proper documentation**

`commit: a2ad710aafa171dfc6974c7121b572ee3ea2033b`

  - add HTML and latex documentation
  - refactor the documentation of publicly visible modules
  - add additional figures and examples of outputs and profiles
  - switch order of initialization of Perun instances and vcs
  - break vcs-params to vcs-flags and vcs-param
  - fix the issue with missing index
  - enhance the performance of Perun (guarding, rewriting to table lookup, or lazy inits)
  - add loading of yaml parameters from CLI

0.10.1 (2017-10-24)
-------------------

**Remodeling of the  regression analysis interface**

`commit: 14ce41c28d4d847ed2c74eac6a2dbfe7644cfd93`

  - refactor the interface of regression analysis
  - update the regression analysis error computation
  - add new parameters for plotting models
  - reduce number of specific computation functions
  - update the architecture (namely the interface)
  - update the documentation of regression analysis and parameters for cli
  - update the regressions analysis error computation
  - add constant model
  - add paging for perun log and status
  - rename converters and transformations modules

0.10 (2017-10-10)
-----------------

**Add Scatter plot visualization module**

`commit: f0d9785639e5c03a994eb439d54206722a455da3`

  - add scatter plot as new visualisation module (basic version with some temporary workarounds)
  - fix bisection method not producing model for some intervals
  - add examples of scatter plot graphs

0.9.2 (2017-09-28)
------------------

**Extend the regression analysis module**

`commit: 12c06251193701356685e8163a7ef8ce8b7d9f2a`

  - add transformation of models to plotable data points
  - add helper functions for plotting models
  - add support of regression analysis extensions

0.9.1 (2017-09-24)
------------------

**Extend the query module**

`commit: bf8ff341cfa942b82093850c63655b79674ea615`

  - add proper testing to query module
  - polish the messy conftest.py
  - add support generators and fixtures for query profiles
  - extend the profile query module with key values and models queries

0.9 (2017-08-31)
----------------

**Add regression analysis postprocessing module**

`commit: 2b3d0d637699ae35b36672df3ce4c14fa0fed701`

  - add regression analysis postprocessor module
  - add example resulting profiles


0.8.3 (2017-08-31)
------------------

`commit: e47f5588e834fd70042bb18ea53a7d76f75cc8b7`

**Update and fix complexity collector**

  - fix several minor issues with complexity collector
  - polish the standard of the generated profile
  - add proper testinr for cli
  - refactor according to the pylint
  - fix bug where vector would not be cleared after printing to file
  - remove code duplication in loop specification
  - fix different sampling data structure for job and complexity cli
  - fix some minor details with cli usage and info output

0.8.2 (2017-07-31)
------------------

**Update the command line interface of complexity collector**

`commit: 1451ae054e77e81bf0aa4930639bf323c09c510e`

  - add new options to complexity collector interface
  - add thorough documentation
  - refactor the implementation

0.8.1 (2017-07-30)
------------------

**Update the performance of command line interface**

`commit: 1fef373e8899b3ff0b0525ec99da91ba7a67fac0`

  - add on demand import of big libraries
  - optimize the memory collector by minimizing subprocess calls
  - fix issue with regex in memory collector
  - add caching of memory collector syscalls
  - extend cli of add and remove to support multiple args
  - extend the massaging of parameters for cli
  - remodel the config command
  - add support for tags in command line
  - enhance the status output of the profile list
  - enhance the default formatting of config
  - add thorough validity checking of bars/flow params

0.8 (2017-07-03)
----------------

**Add flame graph visualization**

`commit: 56a29c807f2d7ad34b7af6002e5ebf90c717e8d7`

  - add flame graph visualization module

0.7.2 (2017-07-03)
------------------

**Refactor flow graph to a more generic form**

`commit: eb33811236575599fc9aa82ce417c492be22d79b`

  - refactor flow to more generic format
  - work with flattened pandas.DataFrame format
  - use set of generators and queries for manipulation with profiles
  - make the cli API generic
  - polish the visual apeal of flow graphs
  - simplify output to bokeh.charts.Area
  - add basic testing of bokeh flow graphs
  - fix the issue with additional layer in memory profs

0.7.1 (2017-06-30)
------------------

**Refactor bar graph to a more generic form**

`commit: 5942e0b1aa8cc09ce0e22b030c3ec17dfdce0556`

  - refactor bars to more generic format
  - work with flattened pandas.DataFrame format
  - make the cli API generic
  - polish the visual apeal of bars graph
  - add unique colour palette to bokeh graphs
  - fix minor issue with matrix in config
  - add massaging of params for show and postprocess

0.7 (2017-06-26)
----------------

**Add bar graph visualization**

`commit: a0f1a4921ecf9ef8f5b7c14ba42442fc589581ed`

  - integrate bar graph visualization

0.6 (2017-06-26)
----------------

**Add Flow graph visualization**

`commit: 5683141b2e622af871eabc1c7259654151177256`

  - integrate flow graph visualization

0.5.1 (2016-06-22)
------------------

**Fix issues in memory collector**

`commit: 28560e8d47cb2b1e2087d7072c44584563f78870`

  - extend the CLI for memory collect
  - annotate phases of memory collect with basic informations
  - add checks for presence of debugging symbols
  - fix in various things in memory collector
  - extend the testing of memory collector

0.5 (2016-06-21)
----------------

**Add Heap map visualization**

`commit: 6ac6e43080f0a9b0c856636ed5ae12ee25a3d4df`

  - integrate Heap map visualization
  - add thorough testing of heap and heat map
  - refactor profile converting
  - refactor duplicate blobs of code
  - add animation feature
  - add origin to profile so it can be compared before adding profile
  - add more smart lookup of the profile for add
  - add choices for collector/vcs/postprocessor parameters in cli
  - simplify adding parameters to collectors/postprocessors
  - add support for formatting strings for profile list
  - refactor log and status function
  - add basic testing for the command line interface
  - switch interactive configuration to using editor
  - implement wrappers for collect and postprocessby
  - rename 'bin' keyword to 'cmd' in stored profiles
  - add basic testing of the collectors and commands

0.4.2 (2017-05-31)
------------------

**Collective fixes mostly for Memory collector**

`commit: 4d94299bc196292284995aabdce0c702e76b33ca`

  - fix a collector issue with zero value addresses
  - add checking validity of the looked up minor version
  - fix issue with incorrect parameter of the NotPerunRepositoryException
  - raise exception when the profile is in incorrect json syntax
  - catch error when minor head could not be found
  - add exception for errors in wrapped VCS
  - add exception for incorrect profile format
  - raise NotPerunRepository, when Perun is not located on path
  - fix message when git was reinitialized
  - catch exceptions for init

0.4.1 (2017-05-15)
------------------

**Collective fixes mosty for Complexity collector**

`commit: 13bebd88613fce58458d50207aea01ee7f672f86`

  - fixed size data container growth if functions were sampled
  - enhance the perun status with info about untracked profiles
  - add colours to printing of profile list (red for untracked)
  - add output of untracked profiles to perun status
  - fix issue with postprocessor parameter rewritten by local variable

0.4 (2017-03-17)
----------------

**Add Complexity collector**

`commit: 323228f95050e52041b47af899eaea6e90eb0605`

  - add complexity collector module


0.3 (2017-03-14)
----------------

**Adding Memory Collector**

`commit: 558ae1eee3acd370c519ac39e774d7fe05d23e35`

  - add memory collector module
  - fix the issue with detached head state and perun status
  - add simple, but interactive, initialization of the local config

0.2 (2017-03-07)
----------------

**Add basic job units**

`commit: 7994b5618eb27684da57ce0941f4f58604ac29ea`

  - add the normalizer postprocessor
  - add the time collector
  - refactor the git module to use the python package
  - add loadinng of config from local yml
  - refactor construction of job matrix
  - remove cmd from job tuple and rename params to args
  - break perun run to run matrix (from config) and run job (from stdout)
  - fix issue of assuming different structure of profile
  - add functionality of creating and storing profiles
  - add generation of the profile name for given job
  - add storing of the profile at given path
  - add generation of profile out of collected data
  - update the params between the phases
  - polish the perun --short header
  - various minor tweaks for outputs
  - change init-vcs-* options to just vcs-*
  - fix an issue with incorrectly outputed comma if no profile type was present
  - fix an issue with loading profile having two modes (compressed and uncompressed)
  - implement base logic for calling collectors and postprocessors
  - enhance output of profile numbers in perun log and status with colours and types
  - add header for short info
  - add colours to the header
  - add base implementation of perun show
  - fix loading of compressed file
  - polish output of perun log and status by adding indent, colours and padding
  - fix an issue with adding non-existent profile
  - fix multiple adding of the same entry
  - fix an issue when the added entry should go to end of index

0.1 (2017-02-22)
----------------

**First partially working implementation**

`commit: 4dd5ee3c638570489d60c50ca41b519029da9007`

  - add short printing of minor version info (--short-minors | -s option)
  - fix reverse output of log (oldest was displayed first)
  - implement simplistic perun log outputing minor version history and profile numbers
  - fix an incorrect warning about already tracked profiles
  - add removal of the entry from the index
  - add registering of  files to the minor version index
  - refactor according to pylint
  - add base implementation of perun log
  - add base implementation of perun status
  - add base implementation of perun add
  - add base implementation of perun rm
  - add base implementation of perun init
  - add base implementation of perun config
  - add base commandline interface through click

0.0 (2016-12-10)
----------------

**Initial minimalistic repository**

`commit: 2a6d1e65e5f3871e091d395789b9fd44450ef9e4`

  - empty root
