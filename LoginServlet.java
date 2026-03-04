import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.sql.*;

public class LoginServlet extends HttpServlet {
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {

        String phone = request.getParameter("phone");
        String pass = request.getParameter("password");

        response.setContentType("text/html");
        PrintWriter out = response.getWriter();

        try {
            // Load SQL Server JDBC Driver
            Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");

            // Database connection URL
            String url = "jdbc:sqlserver://localhost:1433;databaseName=YourDatabaseName;integratedSecurity=true";
            // Use this if using SQL Server authentication:
            // String url = "jdbc:sqlserver://localhost:1433;databaseName=YourDatabaseName";
            // String username = "your_username";
            // String password = "your_password";

            // Connect to the database
            Connection con = DriverManager.getConnection(url);

            // Query to validate user login
            String query = "SELECT * FROM signup8 WHERE phoneno = ? AND password = ?";
            PreparedStatement ps = con.prepareStatement(query);
            ps.setString(1, phone);
            ps.setString(2, pass);

            ResultSet rs = ps.executeQuery();

            if (rs.next()) {
                out.println("<h3>Login Successful</h3>");
                // Redirect to bundles.html
                response.sendRedirect("bundles.html");
            } else {
              
            }

            rs.close();
            ps.close();
            con.close();

        } catch (Exception e) {
            e.printStackTrace();
            out.println("<h3>Error: " + e.getMessage() + "</h3>");
        }
    }
}
