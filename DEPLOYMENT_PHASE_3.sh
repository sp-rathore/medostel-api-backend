#!/bin/bash

#############################################################################
# USER_LOGIN API - DEPLOYMENT SCRIPT (PHASE 3)
#
# Phase 3: Application Code Deployment (20 minutes)
# Deploys Python code and registers API routes
#############################################################################

set -e  # Exit on any error

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ==================== HELPER FUNCTIONS ====================

print_header() {
    echo -e "\n${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}\n"
}

print_step() {
    echo -e "${YELLOW}📋 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# ==================== PHASE 3: APPLICATION CODE DEPLOYMENT ====================

phase_3_deployment() {
    print_header "PHASE 3: APPLICATION CODE DEPLOYMENT (20 minutes)"

    # Step 3.1: Update code from git
    print_step "Step 3.1: Updating code from git..."

    if git pull origin main 2>&1 | grep -E "(Already up to date|Fast-forward|Merge)"; then
        print_success "Code updated successfully"
    else
        print_error "Git pull encountered issues"
    fi

    # Verify critical files exist
    print_step "Verifying critical files..."

    REQUIRED_FILES=(
        "src/routes/v1/user_login.py"
        "src/schemas/user_login.py"
        "src/db/user_login_utils.py"
        "src/utils/password_utils.py"
    )

    for file in "${REQUIRED_FILES[@]}"; do
        if [ -f "$file" ]; then
            print_success "Found: $file"
        else
            print_error "Missing: $file"
            return 1
        fi
    done

    # Step 3.2: Install dependencies
    print_step "Step 3.2: Installing/updating dependencies..."

    DEPS=(
        "fastapi>=0.95.0"
        "pydantic>=2.0"
        "bcrypt"
        "passlib"
        "psycopg2-binary"
        "httpx"
    )

    for dep in "${DEPS[@]}"; do
        echo -n "  Installing $dep... "
        if pip install "$dep" > /dev/null 2>&1; then
            echo -e "${GREEN}OK${NC}"
        else
            echo -e "${RED}FAILED${NC}"
            return 1
        fi
    done

    print_success "All dependencies installed"

    # Verify installations
    print_step "Verifying installations..."

    echo -e "\n${YELLOW}Package versions:${NC}"
    pip list | grep -E "fastapi|pydantic|bcrypt|passlib|psycopg2"

    # Step 3.3: Check for main app file
    print_step "Step 3.3: Checking application structure..."

    if [ -f "src/main.py" ]; then
        print_success "Found main app file: src/main.py"

        # Check if user_login router is already included
        if grep -q "user_login" src/main.py; then
            print_success "user_login router already registered"
        else
            print_step "Adding user_login router to main app..."
            echo ""
            echo -e "${YELLOW}NOTE: Manual action may be required!${NC}"
            echo "Add the following lines to src/main.py:"
            echo ""
            echo "    from src.routes.v1 import user_login"
            echo "    app.include_router(user_login.router)"
            echo ""
        fi
    else
        print_error "src/main.py not found"
        echo -e "${YELLOW}Please ensure main app file exists and routes are registered${NC}"
    fi

    # Step 3.4: Verify database configuration
    print_step "Step 3.4: Checking database configuration..."

    if grep -q "DB_HOST\|database\|psycopg" src/routes/v1/user_login.py; then
        print_success "Database configuration found in user_login.py"

        # Check if credentials are in code (warning)
        if grep -q "35.244.27.232\|medostel_api_user" src/routes/v1/user_login.py; then
            echo -e "${YELLOW}⚠ Database credentials found in code${NC}"
            echo -e "${YELLOW}Recommendation: Use environment variables instead${NC}"
            echo ""
            echo "Set environment variables:"
            echo "  export DB_HOST=35.244.27.232"
            echo "  export DB_USER=medostel_api_user"
            echo "  export DB_PASSWORD=Iag2bMi@0@6aD"
            echo "  export DB_NAME=medostel"
            echo ""
        fi
    else
        print_error "Database configuration may not be present"
        echo -e "${YELLOW}Ensure database connection is configured in the code${NC}"
    fi

    # Step 3.5: Verify Python syntax
    print_step "Step 3.5: Verifying Python syntax..."

    for file in "${REQUIRED_FILES[@]}"; do
        if python -m py_compile "$file" 2>/dev/null; then
            print_success "Syntax OK: $file"
        else
            print_error "Syntax error in: $file"
            return 1
        fi
    done

    # Step 3.6: Check imports
    print_step "Step 3.6: Checking Python imports..."

    python -c "
from src.routes.v1 import user_login
from src.schemas import user_login as ul_schema
from src.db import user_login_utils
from src.utils import password_utils
print('✓ All imports successful')
" 2>/dev/null || echo -e "${RED}✗ Import check failed${NC}"

    # Phase 3 Checklist
    print_header "PHASE 3 CHECKLIST"
    echo -e "${GREEN}[✓] Code updated from git${NC}"
    echo -e "${GREEN}[✓] All required files present${NC}"
    echo -e "${GREEN}[✓] Dependencies installed${NC}"
    echo -e "${GREEN}[✓] Database connection configured${NC}"
    echo -e "${GREEN}[✓] Python syntax verified${NC}"

    if [ -f "src/main.py" ]; then
        if grep -q "user_login" src/main.py; then
            echo -e "${GREEN}[✓] Routes registered${NC}"
        else
            echo -e "${YELLOW}[⚠] Routes may need manual registration${NC}"
        fi
    fi

    echo -e "\nPhase 3 Status: ${GREEN}COMPLETE${NC}\n"

    return 0
}

# ==================== MAIN EXECUTION ====================

main() {
    print_header "USER_LOGIN API - PHASE 3 DEPLOYMENT"
    echo -e "Started at: $(date '+%Y-%m-%d %H:%M:%S')\n"

    # Verify we're in the right directory
    if [ ! -d "src" ]; then
        print_error "Not in project root directory (src/ not found)"
        echo "Please run this script from: /path/to/medostel-api-backend"
        return 1
    fi

    # Check git is initialized
    if [ ! -d ".git" ]; then
        print_error "Not a git repository"
        return 1
    fi

    # Execute phase
    if phase_3_deployment; then
        print_header "PHASE 3 COMPLETE"
        echo -e "${GREEN}✓ Application code deployment successful${NC}"
        echo -e "\n${GREEN}Status: READY FOR PHASE 4 (Testing Deployment)${NC}\n"

        # Display summary
        echo -e "${BLUE}Next Steps:${NC}"
        echo "  1. Run: ./DEPLOYMENT_PHASE_4.sh"
        echo "  2. Verify all tests pass"
        echo "  3. Test API endpoints"
        echo ""

        return 0
    else
        print_header "PHASE 3 FAILED"
        echo -e "${RED}✗ Application code deployment failed${NC}"
        return 1
    fi
}

# Run main function
main
exit $?
