# This Puppet manifest fixes an Apache 500 error by ensuring correct packages, permissions, and configurations.

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
    mode    => '0755', # Only applies to this directory
    recurse => true,
  }

  # Ensure all directories inside /var/www/html have the correct permissions
  exec { 'fix_directories':
    command => "find /var/www/html -type d -exec chmod 0755 {} \\;",
    path    => ['/bin', '/usr/bin'],
  }

  # Ensure all files inside /var/www/html have correct permissions (0644)
  exec { 'fix_files':
    command => "find /var/www/html -type f -exec chmod 0644 {} \\;",
    path    => ['/bin', '/usr/bin'],
  }

  # Restart Apache to apply changes
  exec { 'restart_apache':
    command     => '/usr/sbin/service apache2 restart',
    refreshonly => true,
    subscribe   => [ Package['apache2'], Package['php5'], Package['libapache2-mod-php5'], File['/var/www/html'], Exec['fix_directories'], Exec['fix_files'] ],
  }

}

include apache_fix
