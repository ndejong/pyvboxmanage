# PyVBoxManage

## Example01
```yaml

vars:
  # Define some variables used in the "pyvboxmanage" section below.
  source_vmname: "Ubuntu-20.04-master"
  target_vmname: "Ubuntu-20.04-pipeline"
  target_basefolder: "/opt/virtual-machines"
  target_groups: "/cicd"
  target_bridgeadapter: "enp0s25"


pyvboxmanage:
  # Command opts and args follow https://www.virtualbox.org/manual/ch08.html docs

  # Use stdout from showvminfo to confirm the string "running" is not present, 
  # else stop running.  Permit exit returncodes 0 and 1 to handle situation 
  # where the vmname does not exist yet. 
  - showvminfo:
    args:
      - '{target_vmname}'
    triggers:
      - source: stdout
        string: running
        condition: not present
    returncodes: [0,1]

  # Unregister and delete the existing vmname, also permit exit returncodes 0 
  # and 1 to handle situation where the vmname does not exist yet.
  - unregistervm:
    args: '{target_vmname}'
    opts:
      delete: true
    returncodes: [0,1]

  # Clone a vmname into a defined basefolder and group, also register the VM.  
  # Define a longer than timeout to accomodate the situation where the clone 
  # process takes a long time 
  - clonevm:
    args: '{source_vmname}'
    opts:
      name: '{target_vmname}'
      basefolder: '{target_basefolder}'
      groups: '{target_groups}'
      register: true
      mode: "machine"
    timeout: 300

  # Modify the new VM with 4x network interface cards and make them active. 
  - modifyvm:
    args: '{target_vmname}'
    opts:
      nic1: "bridged"
      nic2: "bridged"
      nic3: "bridged"
      nic4: "bridged"
      bridgeadapter1: '{target_bridgeadapter}'
      bridgeadapter2: '{target_bridgeadapter}'
      bridgeadapter3: '{target_bridgeadapter}'
      bridgeadapter4: '{target_bridgeadapter}'
      nictype1: "82543GC"
      nictype2: "82543GC"
      nictype3: "82543GC"
      nictype4: "82543GC"
      macaddress1: "08002722E901"
      macaddress2: "08002722E902"
      macaddress3: "08002722E903"
      macaddress4: "08002722E904"
      cableconnected1: "on"
      cableconnected2: "on"
      cableconnected3: "on"
      cableconnected4: "on"

  # Start the VM instance and open it in the GUI. 
  - startvm:
    args: '{target_vmname}'
    opts:
       type: "gui"

```
