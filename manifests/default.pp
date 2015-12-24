import "system-packages.pp"
import "mongo.pp"

########################################################################

exec { 'pip-reqs':
    command => '/usr/bin/pip install -U pip fabric simplejson celery celery-with-redis requests pymongo beautifulsoup4 lxml',
    require => [Package['python-pip'], Package['libxml2-dev'], Package['libxslt-dev']],
    #unless => '/usr/bin/env python -c "import simplejson"',
}

########################################################################

file { '/home/ubuntu/milton':
    ensure => 'directory',
    mode => 0775,
    owner => 'ubuntu',
    group => 'ubuntu',
}

########################################################################

$install_dir = '/home/ubuntu/milton'

########################################################################

## Celery Setup ##

file { '/var/log/celery':
    ensure => 'directory',
    mode => 0775,
    owner => 'ubuntu',
    group => 'ubuntu',
}

file { '/var/log/celery/celery.log':
    ensure => 'file',
    mode => 0775,
    owner => 'ubuntu',
    group => 'ubuntu',
    require => [File['/var/log/celery']],
}

file { '/var/run/celery':
    ensure => 'directory',
    mode => 0775,
    owner => 'ubuntu',
    group => 'ubuntu',
}

file { '/etc/default/celeryd':
    target => '/vagrant/conf/celeryd.config',
    ensure => 'link',
}

file { '/etc/init.d/celeryd':
    target => '/vagrant/init.d/celeryd',
    ensure => 'link',
    mode => 0775,
}

service { 'celeryd':
    ensure => running,
    provider => 'upstart',
    require => File['/etc/init.d/celeryd'],
}