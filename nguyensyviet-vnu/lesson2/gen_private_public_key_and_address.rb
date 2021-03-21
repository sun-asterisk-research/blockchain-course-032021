require 'openssl'
require 'securerandom'
require 'digest'
require 'base58'

curve = OpenSSL::PKey::EC.new('secp256k1') #gọi đến chuẩn secp256k1
curve.generate_key
private_key = curve.private_key.to_s(16)
# --------------------------
# Secp256k1 Curve Parameters
# --------------------------
# y^2 = x^3 + ax + b
#theo tài liệu http://www.secg.org/sec2-v2.pdf phần Recommended Parameters secp256k1 với chuẩn secp256k1 có
$a = 0
$b = 7
# prime modulus
$p = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
# number of points on the curve
$n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
# generator point (the starting point on the curve used for all calculations)
$g = {
    x: 55066263022277343669578718895168534326250603453777594175500187360389116729240,
    y: 32670510020758816978083085130507043184471273380659243275938904335757337482424,
  }
  def modinv(a, m = $p)
    a = a % m if a < 0 # make sure a is positive
    prevy, y = 0, 1
    while a > 1
      q = m / a
      y, prevy = prevy - q * y, y
      a, m = m % a, a
    end
    return y
  end
  
  # Double - Add a point on the curve to itself.
  def double(point)
    # slope = (3x^2 + a) / 2y
    slope = ((3 * point[:x] ** 2) * modinv((2 * point[:y]))) % $p # using modular inverse to perform "division"
  
    # new x = slope^2 - 2x
    x = (slope ** 2 - (2 * point[:x])) % $p
  
    # new y = slope * (x - new x) * y
    y = (slope * (point[:x] - x) - point[:y]) % $p
  
    # return x, y coordinates of point
    return { x: x, y: y }
  end
  
  # Add - Add two points together.
  def add(point1, point2)
    # double if both points are the same
    return double(point1) if point1 == point2
  
    # slope = (y1 - y2) / (x1 - x2)
    slope = ((point1[:y] - point2[:y]) * modinv(point1[:x] - point2[:x])) % $p
  
    # new x = slope^2 - x1 - x2
    x = (slope ** 2 - point1[:x] - point2[:x]) % $p
  
    # new y = slope * (x1 - new x) - y1
    y = ((slope * (point1[:x] - x)) - point1[:y]) % $p
  
    # return x, y coordinates of point
    return { x: x, y: y }
  end
  
  # Multiply - Use the double and add operations to quickly multiply a point by an integer (e.g. a private key).
  def multiply(k, point = $g) # multiply the generator point by default
    # create a copy the initial starting point (for use in addition later on)
    current = point
  
    # convert integer to binary representation (for use in the double and add algorithm)
    binary = k.to_s(2)
  
    # double and add algorithm for fast multiplication
    binary.split("").drop(1).each do |char| # ignore first binary character
      # 0 = double
      current = double(current)
  
      # 1 = double and add
      if char == "1"
        current = add(current, point)
      end
    end
  
    # return the final point
    return current
  end
  
  # -------------------------
  # Private Key To Public Key
  # -------------------------
  # convert private key to an integer
  k = private_key.to_i(16)
  
  # multiply generator point by this private key
  point = multiply(k, $g) # this point is the public key
  
  # convert x and y values of this point to hexadecimal
  x = point[:x].to_s(16).rjust(64, "0")
  y = point[:y].to_s(16).rjust(64, "0")
  
  # uncompressed public key format (not used much these days, just showing how it looks)
  public_key_uncompressed = "04" + x + y
  
  # compressed public key format (every x value has a y that could be one of two possible points)
  if (point[:y] % 2 == 0)
    prefix = "02" # if y is even
  else
    prefix = "03" # if y is odd
  end
  
  public_key_compressed = prefix + x # only uses the full x coordinate
  
  # -------
  # Results
  # -------
  puts private_key          
  puts public_key_compressed
  puts public_key_uncompressed
  $version_number = '00'
  def checksum(hex)
    Digest::SHA256.hexdigest(Digest::SHA256.hexdigest(hex))[0...8]
  end
  gen_add_step3 = Digest::SHA256.hexdigest public_key_compressed  
  gen_add_step4 = Digest::RMD160.hexdigest gen_add_step3
  gen_add_step5 = $version_number + gen_add_step3
  gen_add_step6 = Digest::SHA256.hexdigest gen_add_step4  
  gen_add_step7 = Digest::SHA256.hexdigest gen_add_step5  
  gen_add_step8 = checksum(gen_add_step7)
  gen_add_step9 = gen_add_step5 + gen_add_step8
  bitcoin_address = gen_add_step10 = Base58.encode(gen_add_step9.to_i(16))
  puts bitcoin_address

