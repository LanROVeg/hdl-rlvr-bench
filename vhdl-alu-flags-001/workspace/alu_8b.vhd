library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity alu_8b is
    Port (
        A       : in  STD_LOGIC_VECTOR(7 downto 0);
        B       : in  STD_LOGIC_VECTOR(7 downto 0);
        ALU_Sel : in  STD_LOGIC_VECTOR(2 downto 0);
        Result  : out STD_LOGIC_VECTOR(7 downto 0);
        NZVC    : out STD_LOGIC_VECTOR(3 downto 0)
    );
end alu_8b;

architecture Behavioral of alu_8b is
begin
    Result <= (others => '0');
    NZVC   <= (others => '0');
end Behavioral;
