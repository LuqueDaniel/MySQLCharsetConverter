# MySQL Charset Converter
This script generate a script that allow you to  convert the charset of a MySQL database into another one.

* Version: **0.1**
* Licensed under: **GPLv3+**

## Dependencies
* Python: **3+** or **2.7**
* [mysqlclient](https://pypi.python.org/pypi/mysqlclient)

## Example of use
First of all you needs modify ```charset_converter.py```.
```python
#SQL config
db_host = 'yout_host'  # Host address and port
db_user = 'Username'  # Database username
db_password = 'Password'  # User password
db_name = 'database_name'  # Database name
#from_charset = 'latin1'  # Current database character set
from_collation = 'latin1_swedish_ci'  # Current database collation
to_charset = 'utf8'  # Future database character set

#Script Config
gen_script_filename = "output.sql"
```
And then run.
```bash
python charset_converter.py
```
##### Result
```sql
# CHANGE DATABASE CHARACTER SET
ALTER DATABASE wordpress CHARACTER SET utf8;

################################################################################
# wp_commentmeta
################################################################################
# CHANGE DEFAULT TABLE CHARACTER SET
ALTER TABLE wp_commentmeta CHARACTER SET utf8;
# meta_key
alter table wp_commentmeta change meta_key meta_key VARBINARY(255);
alter table wp_commentmeta change meta_key meta_key VARCHAR(255);
# meta_value
alter table wp_commentmeta change meta_value meta_value LONGBLOB;
alter table wp_commentmeta change meta_value meta_value LONGTEXT CHARACTER SET utf8;
```

## To do
* **Catch ENUM**

## License
**[See GPLv3 license.](https://github.com/LuqueDaniel/MySQLCharsetConverter/blob/master/LICENSE)**
