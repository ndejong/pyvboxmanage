# PyVBoxManage

The pyvboxmanage configuration file is forgiving and flexible with several alternative configuration 
attribute names possible.

The input `args` and `opts` for each VBoxManage command follows the Virtual Box documentation
 * https://www.virtualbox.org/manual/ch08.html 

All VBoxManage commands are supported and possible. 

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

## vars
```yaml
vars:
  <var1_name>: <value>
  <var2_name>: '<value>'
  <var3_name>: "<value>"
```
