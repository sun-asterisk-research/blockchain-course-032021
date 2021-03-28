require 'openssl'
require 'securerandom'

class BitcoinAddressGenerator

  ADDRESS_VERSION = '00'  

  def self.generate_address
    #OpenSSL::PKey::EC cung cấp quyền truy cập vào thuật toán ELiptic Curve Digital Signature Algorithm (ECDSA) 
    curve = OpenSSL::PKey::EC.new('secp256k1') #gọi đến chuẩn secp256k1

    # Tạo private key và public key
    curve.generate_key

    private_key_hex = curve.private_key.to_s(16)
    puts "private_key_hex: #{private_key_hex}"    #in ra private key dạng hex
    puts "private_key_wif: #{wif(private_key_hex)}"     #in ra private key dạng WIF

    public_key_hex = curve.public_key.to_bn.to_s(16)    #phương thức to_bn sử dụng để convert point trên đường cong thành Big number
    puts "public_key_hex: #{public_key_hex}"    #in ra pulic key dạng hex

    pub_key_hash = public_key_hash(public_key_hex)
    puts "pub_key_hash: #{pub_key_hash}"    #in ra public key dạng hash

    address = generate_address_from_public_key_hash(pub_key_hash)

    puts "address: #{address}"    #in ra địa chỉ
  end

  def self.generate_address_from_public_key_hash(pub_key_hash)
    pk = ADDRESS_VERSION + pub_key_hash
    encode_base58(pk + checksum(pk))
  end

  def self.int_to_base58(int_val, leading_zero_bytes=0)
    alpha = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    base58_val, base = '', alpha.size
    while int_val > 0
      int_val, remainder = int_val.divmod(base)
      base58_val = alpha[remainder] + base58_val
    end
    base58_val
  end

  def self.encode_base58(hex)
    leading_zero_bytes = (hex.match(/^([0]+)/) ? $1 : '').size / 2
    ("1"*leading_zero_bytes) + int_to_base58( hex.to_i(16) )
  end

  def self.checksum(hex)
    sha256(sha256(hex))[0...8]
  end

  PRIV_KEY_VERSION = '80'
  def self.wif(hex)
    data = PRIV_KEY_VERSION + hex
    encode_base58(data + checksum(data))
  end

  # RIPEMD-160 (160 bit) hash
  def self.rmd160(hex)
    Digest::RMD160.hexdigest([hex].pack("H*"))
  end

  def self.sha256(hex)
   Digest::SHA256.hexdigest([hex].pack("H*"))
  end

  # Chuyển public key thành dạng 160 bit public key hash
  def self.public_key_hash(hex)     
    rmd160(sha256(hex))    #sha256 trước khi băm rmd160
  end
end

BitcoinAddressGenerator.generate_address

# Bài viết tham khảo: https://bhelx.simst.im/articles/generating-bitcoin-keys-from-scratch-with-ruby/


