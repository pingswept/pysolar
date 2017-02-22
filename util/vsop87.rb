#!/usr/local/bin/ruby
require 'date'
require 'cgi'

# doc
class Clock
  def initialize(date)
    date = date.utc
    @date = date
    @year = date.year
    @month = date.month
    @day = date.day
    @hour = date.hour
    @min = date.min
    @sec = date.sec
    @time_in_day = @hour.to_f / 24 + @min.to_f / 1140 + @sec.to_f / 86_400
    @time_in_hour = @hour.to_f + @min.to_f / 60 + @sec.to_f / 3600
    @time_in_sec = @hour * 3600 + @min * 60 + @sec
  end

  def jd
    if @month <= 2
      y = (@year - 1).to_i
      m = (@month + 12).to_i
    else
      y = @year
      m = @month
    end

    julian_day = (
      365.25 * (y + 4716)).floor + (30.6001 * (m + 1)).floor + @day - 1524.5

    if julian_day < 2_299_160.5
      transition_offset = 0
    else
      tmp = (@year / 100).floor
      transition_offset = 2 - tmp + (tmp / 4).floor
    end

    julian_day + transition_offset
  end
end
# doc
class SplitData
  def initialize(data)
    @data_array = []
    @data = data
  end

  def split
    @data_array << @data[1..1].to_i # version
    @data_array << @data[2..2].to_i # body
    @data_array << @data[3..3].to_i # index
    @data_array << @data[4..4].to_i # alpha
    @data_array << @data[79..96].to_f # A
    @data_array << @data[97..110].to_f # B
    @data_array << @data[111..130].to_f # C
    @data_array
  end
end
# doc
class VSOP87
  def initialize(data_set, jd)
    @data_set = data_set
    @jd = jd
  end

  def load
    data_array = []
    open(@data_set) do |file|
      while line = file.gets
        if line[1..1] != 'V'
          r = SplitData.new(line)
          data_array << r.split
        end
      end
    end
    data_array
  end

  def calc
    data_array = load
    t = ((@jd - 2_451_545.0) / 365_250).to_f
    v = []
    data_array.each do |data|
      i = data[2] - 1
      v[i] = 0 if v[i].nil?
      v[i] = v[i].to_f + (
        t**data[3]) * data[4].to_f * Math.cos(data[5].to_f + data[6].to_f * t)
    end
    v
  end
end

#

input = CGI.new
data_set = input['f']
jd = input['d']
print "Content-type:text/plain\n\n"
if data_set
  unless jd
    date = Time.now
    time = Clock.new(date)
    jd = time.jd
  end
  jd.to_f
  vsop = VSOP87.new(data_set, jd)
  puts "#{data_set} at JD#{jd}"
  v_array = vsop.calc
  i = 0
  v_array.each do |v|
    puts "variable[#{i}] =  #{v}"
    i += 1
  end
else
  f = open('./VSOP87D.ear.txt')
  description = f.read
  f.close

  print <<EOS
============
Planetary positions by VSOP87 theory
============

DESCRIPTION
===========

Loading source files of VSOP87 and calculating positions of the planet at given julian day.

USAGE
=========

vsop87.rb?f=FILE_NAME(&d=JULIAN_DAY)

if you omit param "d" you will get current position.

REFERENCE
=========

VI/81 Planetary Solutions VSOP87 (Bretagnon+, 1988)
http://cdsarc.u-strasbg.fr/viz-bin/ftp-index?VI/81


Source Code
=========

http://www.lizard-tail.com/isana/lab/astro_calc/vsop87/vsop87_rb.txt


### Here is the description of VSOP87 files. ###

#{description}

EOS
end
