# pascaltocsv
Convert pascal voc xml files to Google cloud vision object detection dataset csv

### How to use
```
py pascaltocsv.py <xml_directory_path> <bucket_name> <filename>
```

<dl>
  <dt>xml_directory_path</dt>
  <dd>The directory path to pascal voc xml files</dd>
  <dt>bucket_name</dt>
  <dd>Google cloud storage bucket name</dd>
  <dt>filename<dt>
  <dd>File name to generate</dd>
</dl>

### Example

```
py pascaltocsv.py data/pascal_voc_xml mybucket dataset.csv
```

