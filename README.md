# SiLA Qmix
SiLA 2 drivers for CETONI Qmix devices

## Generate the prototype code from the FDL
1. Create a `service_description.json` file in the desired target directory
2. Then run the code generator from the root directory with the following command
   ```console
   $ silacodegenerator -b -o <target_dir> --service-description ../<target_dir>/service_description features/
   ```
   
   E.g. to generate the code for the 'pumps/contiflow' category you'd need to run
   ```
   $ silacodegenerator -b -o pumps/contiflowpumps --service-description ../pumps/contiflowpumps/service_description features/
   ```
3. After that move the directories that contain the implementation classes for each feature into the correct directory in `impl/de/cetoni/`
4. Fix the import paths and implement the features

## Running:
Make sure to have `sila2lib` installed (`pip install sila2lib`) and activated the correct virtualenv (if applicable).

### Windows:
```cmd
> python sila_qmix.py <path-to-qmix-config>
```

### Linux:
```console
$ ./sila_qmix.sh <path-to-qmix-config>
```
