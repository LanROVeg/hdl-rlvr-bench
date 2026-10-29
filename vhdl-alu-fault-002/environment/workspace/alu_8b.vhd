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
    process(A, B, ALU_Sel)
        variable u_a, u_b : unsigned(8 downto 0);
        variable u_res    : unsigned(8 downto 0);
        variable res_v    : std_logic_vector(7 downto 0);
        variable n_flag, z_flag, v_flag, c_flag : std_logic;
    begin
        u_a := '0' & unsigned(A);
        u_b := '0' & unsigned(B);
        res_v  := (others => '0');
        v_flag := '0';
        c_flag := '0';

        case ALU_Sel is
            when "000" => -- ADD (Correct)
                u_res  := u_a + u_b;
                res_v  := std_logic_vector(u_res(7 downto 0));
                c_flag := u_res(8);
                v_flag := (A(7) and B(7) and (not res_v(7))) or ((not A(7)) and (not B(7)) and res_v(7));
            when "001" => -- SUB (Correct)
                u_res  := u_a - u_b;
                res_v  := std_logic_vector(u_res(7 downto 0));
                if unsigned(A) < unsigned(B) then c_flag := '1'; else c_flag := '0'; end if;
                v_flag := (A(7) and (not B(7)) and (not res_v(7))) or ((not A(7)) and B(7) and res_v(7));
            when "010" => -- BUG 1: Swapped AND to OR
                res_v := A or B; 
            when "011" => -- BUG 1: Swapped OR to AND
                res_v := A and B;
            when "100" => res_v := A xor B;
            when "101" =>
                res_v  := A(6 downto 0) & '0';
                c_flag := A(7);
            when "110" => -- BUG 2: Shift Right shifts by 2 instead of 1, wrong carry
                res_v  := "00" & A(7 downto 2); 
                c_flag := A(7); 
            when others => res_v := A;
        end case;

        n_flag := res_v(7);
        if res_v = x"FF" then -- BUG 3: Inverted zero check (checks for all 1s instead of 0s)
            z_flag := '1'; 
        else 
            z_flag := '0'; 
        end if;

        Result <= res_v;
        NZVC   <= n_flag & z_flag & v_flag & c_flag;
    end process;
end Behavioral;
