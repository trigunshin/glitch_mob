exec { 'apt-get-update':
    command => '/usr/bin/apt-get update'
}

# run apt-get update before package installs
Exec['apt-get-update'] -> Package <| |>

package { 'unzip':
    ensure => 'installed'
}
package { 'screen':
    ensure => 'installed'
}
#package { 'git-core':
#    ensure => 'installed'
#}
package { 'curl':
    ensure => 'installed'
}
package { 'python-setuptools':
    ensure => 'installed'
}
package { 'python-pip':
    ensure => 'installed'
}
package { 'python-virtualenv':
    ensure => 'installed'
}
package { 'python-dev':
    ensure => 'installed'
}
package { 'libxml2-dev':
    ensure => 'installed'
}
package { 'libxslt-dev':
    ensure => 'installed'
}