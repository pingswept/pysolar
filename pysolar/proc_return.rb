# adapted from http://eli.thegreenplace.net/2006/04/18/understanding-ruby-blocks-procs-and-methods/

def gen_times(factor)
  p factor
  proc { |n| n * factor }
end

times3 = gen_times(3)
times5 = gen_times(5)

puts times3.call(12)               #=> 36
puts times5.call(5)                #=> 25
