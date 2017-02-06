
require 'date'

def calc(jdn)
  jct = (jdn - 2_451_120) / 36_525.0
  loan = (125.0445222 + jct * (
  -1934.136260833 + jct * (
  0.0020708333 + jct * 2.222e-06))) % 360.0
  mls = (280.4664567 + jct * (
    36_000.76982779 + jct * (
      0.0003032028 + jct * (
        1.0 / 49_931.0 + jct * (
          1.0 / -15_299.0 + jct * (
            1.0 / -1_988_000.0)))))) % 360.0
  [loan, mls]
end

# puts Date.parse('2005-01-01').jd
# puts Date.parse('2018-01-01').jd
(2_455_825..2_458_971).each do |jdn|
  loan = calc(jdn)[0]
  mls = calc(jdn)[1]
  # puts "on #{jdn}, #{loan}, #{mls}"
end

(2_453_396..2_453_398).each do |jdn|
  loan = calc(jdn)[0]
  mls = calc(jdn)[1]
  puts "on #{DateTime.jd(jdn + 0.5)}, #{loan}, #{mls}"
end
puts
(2_453_743..2_453_745).each do |jdn|
  loan = calc(jdn)[0]
  mls = calc(jdn)[1]
  puts "on #{DateTime.jd(jdn + 0.5)}, #{loan}, #{mls}"
end
puts
(2_454_089..2_454_091).each do |jdn|
  loan = calc(jdn)[0]
  mls = calc(jdn)[1]
  puts "on #{DateTime.jd(jdn + 0.5)}, #{loan}, #{mls}"
end
puts
(2_454_783..2_454_785).each do |jdn|
  loan = calc(jdn)[0]
  mls = calc(jdn)[1]
  puts "on #{DateTime.jd(jdn + 0.5)}, #{loan}, #{mls}"
end
puts
(2_455_129..2_455_131).each do |jdn|
  loan = calc(jdn)[0]
  mls = calc(jdn)[1]
  puts "on #{DateTime.jd(jdn + 0.5)}, #{loan}, #{mls}"
end
puts
(2_455_476..2_455_478).each do |jdn|
  loan = calc(jdn)[0]
  mls = calc(jdn)[1]
  puts "on #{DateTime.jd(jdn + 0.5)}, #{loan}, #{mls}"
end
puts
(2_455_823..2_455_825).each do |jdn|
  loan = calc(jdn)[0]
  mls = calc(jdn)[1]
  puts "on #{DateTime.jd(jdn + 0.5)}, #{loan}, #{mls}"
end
