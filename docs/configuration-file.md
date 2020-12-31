# PyVBoxManage

The pyvboxmanage configuration file is forgiving and flexible with several alternative configuration 
attribute names possible.

Variables can be set by declaring `vars`

Configurations can import other configuration files by declaring `imports` 

The input `args` and `opts` for each VBoxManage command follows the Virtual Box documentation
 * https://www.virtualbox.org/manual/ch08.html 

All VBoxManage commands are supported and possible. 

## vars
```yaml
vars:
  <var1_name>: <value>
  <var2_name>: '<value>'
  <var3_name>: "<value>"
  ...
  <varN_name>: "<value>"
```

## imports
```yaml
imports:
  - <pyvboxmanage-config-filename-1.yml>
  - <pyvboxmanage-config-filename-2.yml>
  ...
  - <pyvboxmanage-config-filename-N.yml>
```

## pyvboxmanage
```yaml
pyvboxmanage:
  - <command>:
    arguments|args: <list|string>
    options|opts: <dict>
    outputs|out: <list|string>
    returncodes|returncode: <listofint|int>
    triggers|trigger: <listofdict|dict>
    timeout: <int>
```
