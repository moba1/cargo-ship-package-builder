ln -sfnv /run /var/run
ln -sfvn /run/lock /var/lock


install -dv -m 0750 "$1/root"
install -dv -m 1777 "$1/tmp" "$1/var/tmp"

touch /var/log/{btmp,lastlog,faillog,wtmp}
chgrp -v utmp /var/log/lastlog
chmod -v 664 /var/log/lastlog
chmod -v 600 /var/log/btmp
