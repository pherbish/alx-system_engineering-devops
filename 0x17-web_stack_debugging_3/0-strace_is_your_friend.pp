# This Puppet manifest fixes an Apache 500 error by ensuring necessary packages, permissions, and configurations are set correctly.

class apache_fix {
  
  # Ensure Apache is installed
  package { 'apache2':
    ensure => installed,
  }

  # Ensure PHP is installed (modify the version as needed)
  package { 'php5':
    ensure => installed,
  }

  # Ensure necessary PHP modules are installed
  package { 'libapache2-mod-php5':
    ensure  => installed,
    require => Package['php5'],
  }

  # Ensure Apache service is running
  service { 'apache2':
    ensure    => running,
    enable    => true,
    require   => Package['apache2'],
  }

  # Ensure correct permissions for web directory
  file { '/var/www/html':
    ensure  => directory,
    owner   => 'www-data',
    group   => 'www-data',
    mode    => '0755',
    recurse => true,
  }

  # Restart Apache to apply changes
  exec { 'restart_apache':
    command     => '/usr/sbin/service apache2 restart',
    refreshonly => true,
    subscribe   => [ Package['apache2'], Package['php5'], Package['libapache2-mod-php5'], File['/var/www/html'] ],
  }

}

include apache_fix

