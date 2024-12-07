import React from "react";
import { Layout, Menu, Input, Button } from "antd";
import { SearchOutlined, LoginOutlined } from "@ant-design/icons";
import "./Menubar.css";

const { Header } = Layout;

const Navbar = () => {
    return (
        <Header className="navbar navbar-container">
            {/* Section I: Logo and Menu */}
            <div className="navbar-section navbar-left">
                <img src="./logo.png" alt="UAEMéx Logo" className="navbar-logo"/>

                <Menu
                    mode="horizontal"
                    theme="dark"
                    className="navbar-menu"
                    style={{backgroundColor: "transparent"}}
                >
                    <Menu.Item key="home">Inicio</Menu.Item>
                    <Menu.SubMenu key="movilidad" title="Movilidad">
                        <Menu.Item key="intrainstitucional">Intrainstitucional</Menu.Item>
                        <Menu.Item key="nacional">Nacional</Menu.Item>
                        <Menu.Item key="internacional">Internacional</Menu.Item>
                    </Menu.SubMenu>
                </Menu>
            </div>

            {/* Section II: Search Bar */}
            <div className="navbar-section navbar-middle">
                <Input
                    placeholder="Buscar..."
                    allowClear
                    prefix={<SearchOutlined />}
                    className="search-input"
                />
            </div>

            {/* Section III: Login Button */}
            <div className="navbar-section navbar-right">
                <Button
                    type="primary"
                    icon={<LoginOutlined />}
                    className="login-btn"
                >
                    Login
                </Button>
            </div>
        </Header>
    );
};

export default Navbar;
