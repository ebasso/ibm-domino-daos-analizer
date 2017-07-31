This script get output from IBM Domino - DAOS Estimator and generate a customized report
```
Usage: AnalyzeDaos.py -i <inputfile> -o <outputfile>
```

Setup:

1) Download and install DAOS Estimator on your IBM Domino server

2) [Optional] Define notes.ini variable

```
DAOSEST_BUCKETS=32,64,128,256,512,640,768,1024,2048,3072
```

2) Run command

```
load daosest -c -o daosest_<serverName>.txt
```

 The -c will generate a file like DAOSEST_26_07_2017_09_17_40.csv
 
3) Run python script

```
python AnalyzeDaos.py -i /notesdata/DAOSEST_26_07_2017_09_17_40.csv -o /tmp/output.txt
```
 
You can check console or file output.txt
```
===============================================================================
Server Report
|- Databases Count :  5640
|- Databases Size  :   1.30 TB 
|- Attachments Count Total :  1784615
|- Attachments Size Total :  767.30 GB 
|- Attachments Size % :     57.44 
|-- Sizes (KB)       :|     0<=32 |    32<=64 |   64<=128 |  128<=256 |  256<=512 |  512<=640 |  640<=768 | 768<=1024 |    > 1024 |
|-- Atts Count       :|    821738 |    204057 |    202048 |    159355 |    138845 |     39716 |     29336 |     38377 |    151143 |
|-- Atts Count %     :|     46.05 |     11.43 |     11.32 |      8.93 |      7.78 |      2.23 |      1.64 |      2.15 |      8.47 |
|-- Atts Sizes       :|   8.16 GB |   9.07 GB |  18.03 GB |  28.16 GB |  48.29 GB |  21.72 GB |  19.61 GB |  32.46 GB | 581.81 GB |
|-- Atts Sizes %     :|      1.06 |      1.18 |      2.35 |      3.67 |      6.29 |      2.83 |      2.56 |      4.23 |     75.83 |
|
|-- Daos Sizes       :| 767.30 GB | 759.15 GB | 750.08 GB | 732.05 GB | 703.89 GB | 655.60 GB | 633.89 GB | 614.27 GB | 581.81 GB |
|-- Daos Sizes %     :|    100.00 |     98.94 |     97.76 |     95.41 |     91.74 |     85.44 |     82.61 |     80.06 |     75.83 |
===============================================================================
```

