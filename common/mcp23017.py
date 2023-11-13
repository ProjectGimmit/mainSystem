import smbus
import time


class MCP23017:
    """
    ### MCP23017

    「BANK=0」で使用してください
    """

    CHANNEL = 1  # i2c割り当てチャンネル 1 or 0
    REG_IODIRA = 0x00  # GPIOA 入出力設定レジスタ
    REG_GPIOA = 0x12  # GPIOA 入出力レジスタ
    REG_IODIRB = 0x01  # GPIOA 入出力設定レジスタ
    REG_GPIOB = 0x13  # GPIOA 入出力レジスタ
    # I2CADDR : I2Cアドレス

    ##################
    # コンストラクタ #
    ##################
    def __init__(self, I2CADDR):
        # SMBusインスタンスを作成
        self.bus = smbus.SMBus(self.CHANNEL)
        # I2Cアドレスを保存
        self.I2CADDR = I2CADDR

    ###############
    # GPIOAの設定 #
    ###############
    def GPIO_A_init(self, IOADDR) -> None:
        """
        ### GPIOAの入出力設定

        Parameters
        ----------
        IOADDR : bin, hex
          入出力設定アドレス
        """

        # 入出力設定アドレスを書き込み
        self.bus.write_byte_data(self.I2CADDR, self.REG_IODIRA, IOADDR)

    ######################
    # GPIOA 入力状態取得 #
    ######################
    def GPIO_A_input(self, port: int) -> bool:
        """
        ### 指定したポートの入力状態を取得する

        Parameters
        ----------
        port : int
          ポートの位置 0〜7

        Returns
        -------
        入力ON: False
        入力OFF: True
        """

        # 取得したいポート位置を2進数に変換し、ビットマスクを作成
        binary_value = int(bin(1 << port), 2)
        # 現在の入力状態を取得
        decimal_number = self.bus.read_byte_data(self.I2CADDR, self.REG_GPIOA)
        # ビットマスクと現在の入力状態を論理積
        # 入力：False, 未入力：True
        return bool(decimal_number & binary_value)

    ##################
    # GPIOA 出力操作 #
    ##################
    def GPIO_A_output(self, port, on) -> None:
        """
        ### 指定したポートの出力状態を変更する

        Parameters
        ----------
        port : int
          ポートの位置 0〜7
        on : 1, 0
          ON : 1, OFF: 0
        """

        # 操作するポート位置を2進数に変換し、ビットマスクを作成
        binary_value = int(bin(1 << port), 2)
        # 出力の状態を取得
        decimal_number = self.bus.read_byte_data(self.I2CADDR, self.REG_GPIOA)

        if on == 1:  # 出力ON
            # 操作する2進数と現在の出力状態を論理和
            piyo = decimal_number | binary_value
            # アドレス書き込み
            self.bus.write_byte_data(self.I2CADDR, self.REG_GPIOA, piyo)

        else:  # 出力OFF
            # 排他的論理和でビットマスクを作成
            mask = binary_value ^ 0b11111111
            # ビットマスクと現在の出力状態を論理積
            piyo = decimal_number & mask
            # アドレス書き込み
            self.bus.write_byte_data(self.I2CADDR, self.REG_GPIOA, piyo)

    ###############
    # GPIOBの設定 #
    ###############
    def GPIO_B_init(self, IOADDR) -> None:
        """
        ### GPIOAの入出力設定

        Parameters
        ----------
        IOADDR : bin, hex
          入出力設定アドレス
        """

        # 入出力設定アドレスを書き込み
        self.bus.write_byte_data(self.I2CADDR, self.REG_IODIRB, IOADDR)

    ######################
    # GPIOA 入力状態取得 #
    ######################
    def GPIO_B_input(self, port: int) -> bool:
        """
        ### 指定したポートの入力状態を取得する

        Parameters
        ----------
        port : int
          ポートの位置 0〜7

        Returns
        -------
        入力ON: False
        入力OFF: True
        """

        # 取得したいポート位置を2進数に変換し、ビットマスクを作成
        binary_value = int(bin(1 << port), 2)
        # 現在の入力状態を取得
        decimal_number = self.bus.read_byte_data(self.I2CADDR, self.REG_GPIOB)
        # ビットマスクと現在の入力状態を論理積
        # 入力：False, 未入力：True
        return bool(decimal_number & binary_value)

    ##################
    # GPIOA 出力操作 #
    ##################
    def GPIO_B_output(self, port, on) -> None:
        """
        ### 指定したポートの出力状態を変更する

        Parameters
        ----------
        port : int
          ポートの位置 0〜7
        on : 1, 0
          ON : 1, OFF: 0
        """

        # 操作するポート位置を2進数に変換し、ビットマスクを作成
        binary_value = int(bin(1 << port), 2)
        # 出力の状態を取得
        decimal_number = self.bus.read_byte_data(self.I2CADDR, self.REG_GPIOB)

        if on == 1:  # 出力ON
            # 操作する2進数と現在の出力状態を論理和
            out_addr = decimal_number | binary_value
            # アドレス書き込み
            self.bus.write_byte_data(self.I2CADDR, self.REG_GPIOB, out_addr)

        else:  # 出力OFF
            # 排他的論理和でビットマスクを作成
            mask = binary_value ^ 0b11111111
            # ビットマスクと現在の出力状態を論理積
            out_addr = decimal_number & mask
            # アドレス書き込み
            self.bus.write_byte_data(self.I2CADDR, self.REG_GPIOB, out_addr)
