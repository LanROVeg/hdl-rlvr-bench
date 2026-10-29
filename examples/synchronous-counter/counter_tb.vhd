library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use std.env.all;
entity counter_tb is end;
architecture test of counter_tb is
    signal clk, rst, load, enable : std_logic := '0';
    signal data, q : std_logic_vector(7 downto 0) := (others => '0');
begin
    dut: entity work.counter_8b port map(clk,rst,load,enable,data,q);
    process
        variable expected, incoming, checked : integer := 0;
    begin
        rst <= '1'; wait for 1 ns; clk <= '1'; wait for 1 ns;
        assert q=x"00" report "Reset did not clear count" severity failure;
        clk <= '0'; rst <= '0'; wait for 1 ns;
        for seed in 0 to 255 loop
            for controls in 0 to 7 loop
                -- Seed every possible prior state through a synchronous load.
                rst <= '0'; load <= '1'; enable <= '0';
                data <= std_logic_vector(to_unsigned(seed,8));
                wait for 1 ns; clk <= '1'; wait for 1 ns;
                assert q=std_logic_vector(to_unsigned(seed,8)) report "Load failed" severity failure;
                clk <= '0'; wait for 1 ns;
                incoming := (seed*73+controls*29) mod 256;
                data <= std_logic_vector(to_unsigned(incoming,8));
                if controls mod 2=1 then rst <= '1'; else rst <= '0'; end if;
                if (controls/2) mod 2=1 then load <= '1'; else load <= '0'; end if;
                if (controls/4) mod 2=1 then enable <= '1'; else enable <= '0'; end if;
                wait for 1 ns;
                assert q=std_logic_vector(to_unsigned(seed,8))
                    report "Output changed without a rising edge (reset must be synchronous)" severity failure;
                expected := seed;
                if controls mod 2=1 then expected := 0;
                elsif (controls/2) mod 2=1 then expected := incoming;
                elsif (controls/4) mod 2=1 then expected := (seed+1) mod 256; end if;
                clk <= '1'; wait for 1 ns;
                assert q=std_logic_vector(to_unsigned(expected,8))
                    report "Priority, increment, wrap, or hold mismatch" severity failure;
                clk <= '0'; wait for 1 ns;
                assert q=std_logic_vector(to_unsigned(expected,8))
                    report "Output changed on falling edge" severity failure;
                checked := checked+1;
            end loop;
        end loop;
        report "PASS: counter " & integer'image(checked) & " prior-state/control combinations";
        finish;
    end process;
end;
