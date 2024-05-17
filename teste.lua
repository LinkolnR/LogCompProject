function fatorial(n)
    print(n)
    if n == 0 then
        return 1
    else
        return n * fatorial(n - 1)
    end
end
local a
local b
a = 3
b = fatorial(a)
print(a)
print(b)