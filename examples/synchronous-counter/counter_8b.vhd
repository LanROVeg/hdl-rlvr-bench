library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- AI-assisted practice reference: synchronous reset > load > enable > hold.
entity counter_8b is
    port (clk, rst, load, enable : in std_logic;
          data : in std_logic_vector(7 downto 0);
          q : out std_logic_vector(7 downto 0));
end;

architecture rtl of counter_8b is
    signal count : unsigned(7 downto 0);
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' then
                count <= (others => '0');
            elsif load = '1' then
                count <= unsigned(data);
            elsif enable = '1' then
                count <= count + 1;
            end if;
        end if;
    end process;
    q <= std_logic_vector(count);
end;
